#!/usr/bin/env python3
"""
auditar_fugas.py
Busca "trampas" / fugas de información entre splits y hacia la evaluación:

 1. Escena compartida: la MISMA escena/imagen aparece en train y en val/test
    (p.ej. un 'edit' en train que parte de la escena de un 'creation' del test).
 2. Prompts idénticos o casi idénticos entre splits (similitud de n-gramas).
 3. Código de respuesta idéntico o casi idéntico entre splits.
 4. Prompts de generalización (EVALUATION/generar_con_modelo.py) vs. train.
 5. Pistas en el prompt: nombres de funciones del DSL o código dentro del pedido
    de un 'creation'.
 6. Uso de funciones del DSL que no existen (el dataset enseñaría a inventar).

Uso: python DATASET/tools/auditar_fugas.py
Salida: DATASET/reports/auditoria_fugas.json + resumen
"""
import os, re, sys, json, collections, ast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "EVALUATION"))
DATA = os.path.join(ROOT, "TRAINING", "data")


def leer(path):
    s = open(path, encoding="utf-8").read()
    dec, i, rows = json.JSONDecoder(), 0, []
    while i < len(s):
        while i < len(s) and s[i] in " \n\t\r,[]":
            i += 1
        if i >= len(s):
            break
        o, i = dec.raw_decode(s, i)
        rows.append(o)
    return rows


def norm(t):
    t = t.lower().replace("<image>", "")
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"[^\wáéíóúñü ]", " ", t)).strip()


def shingles(t, n=5):
    w = t.split()
    return {" ".join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def jacc(a, b):
    return len(a & b) / max(1, len(a | b))


def codigo_norm(c):
    c = re.sub(r"#.*", "", c)
    c = re.sub(r"(['\"]).*?\1", "S", c)          # nombres/strings no cuentan
    return re.sub(r"\s+", " ", c).strip()


def escena_de(r):
    mm = r.get("multimodal") or {}
    img = mm.get("image") or ""
    return img.split("/")[1] if "/" in img else None


def ultimo_pedido(r):
    us = [m["content"] for m in r["messages"] if m["role"] == "user"]
    return us[-1] if us else ""


def respuesta(r):
    a = [m["content"] for m in r["messages"] if m["role"] == "assistant"]
    return a[-1] if a else ""


def main():
    splits = {sp: leer(os.path.join(DATA, f"{sp}_multimodal.jsonl")) for sp in ("train", "validation", "test")}
    rep = {}

    # 1. Escenas compartidas
    esc = {sp: collections.defaultdict(list) for sp in splits}
    for sp, rows in splits.items():
        for r in rows:
            e = escena_de(r)
            if e:
                esc[sp][e].append((r["id"], r["task_type"]))
    for a, b in (("train", "test"), ("train", "validation"), ("validation", "test")):
        comunes = set(esc[a]) & set(esc[b])
        filas_b = sum(len(esc[b][e]) for e in comunes)
        rep[f"escenas_{a}_{b}"] = {"escenas_comunes": len(comunes), "escenas_en_" + b: len(esc[b]),
                                   "filas_" + b + "_afectadas": filas_b,
                                   "ejemplos": [(e, esc[a][e][:2], esc[b][e][:2]) for e in sorted(comunes)[:5]]}

    # 2/3. Prompts y código casi duplicados (test/val vs train)
    tr = splits["train"]
    tr_p = [shingles(norm(ultimo_pedido(r))) for r in tr]
    tr_c = [shingles(codigo_norm(respuesta(r)), 8) for r in tr]
    tr_c_exact = collections.Counter(codigo_norm(respuesta(r)) for r in tr)
    tr_p_exact = collections.Counter(norm(ultimo_pedido(r)) for r in tr)
    for sp in ("validation", "test"):
        sims_p, sims_c, exact_p, exact_c, top = [], [], 0, 0, []
        for r in splits[sp]:
            p = norm(ultimo_pedido(r)); c = codigo_norm(respuesta(r))
            exact_p += p in tr_p_exact
            exact_c += c in tr_c_exact
            sp_ = shingles(p); sc = shingles(c, 8)
            bp = max(((jacc(sp_, x), i) for i, x in enumerate(tr_p)), default=(0, -1))
            bc = max(jacc(sc, x) for x in tr_c)
            sims_p.append(bp[0]); sims_c.append(bc)
            if bp[0] > 0.8:
                top.append((r["id"], tr[bp[1]]["id"], round(bp[0], 2)))

        def dist(v):
            v = sorted(v)
            return {"mediana": round(v[len(v) // 2], 3), "p90": round(v[int(len(v) * .9)], 3),
                    ">0.8": sum(x > 0.8 for x in v), ">0.95": sum(x > 0.95 for x in v), "n": len(v)}
        rep[f"similitud_{sp}_vs_train"] = {"prompt_identico": exact_p, "codigo_identico": exact_c,
                                           "prompt_jaccard": dist(sims_p), "codigo_jaccard": dist(sims_c),
                                           "pares_prompt_>0.8": top[:10]}

    # 4. Generalización vs train
    from generar_con_modelo import GENERALIZACION
    gen = []
    for gid, p in GENERALIZACION:
        s = shingles(norm(p), 3)
        best = max(((jacc(s, shingles(norm(ultimo_pedido(r)), 3)), r["id"]) for r in tr))
        gen.append({"id": gid, "max_jaccard_train(3-gramas)": round(best[0], 3), "mas_parecido": best[1]})
    rep["generalizacion_vs_train"] = gen
    pisos = collections.Counter()
    for r in tr:
        for m in re.finditer(r"(\d+)\s*pisos", ultimo_pedido(r)):
            pisos[int(m.group(1))] += 1
    rep["pisos_en_train"] = dict(sorted(pisos.items()))

    # 5. Pistas en el prompt de creation
    pistas = collections.Counter()
    ej = []
    for sp, rows in splits.items():
        for r in rows:
            if r["task_type"] != "creation":
                continue
            u = ultimo_pedido(r)
            f = re.findall(r"\b(?:A\.)?(crear_\w+|agregar_\w+)\s*\(", u) or re.findall(r"blender_arch|import bpy", u)
            if f:
                pistas[sp] += 1
                if len(ej) < 5:
                    ej.append((r["id"], f[:3]))
    rep["creation_con_codigo_o_funciones_en_prompt"] = dict(pistas) | {"ejemplos": ej}

    # 6. Funciones del DSL usadas vs existentes
    src = open(os.path.join(ROOT, "DSL", "blender", "blender_arch.py"), encoding="utf-8").read()
    existentes = {n.name for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}
    usadas = collections.Counter()
    for rows in splits.values():
        for r in rows:
            for m in r["messages"]:
                if m["role"] == "assistant":
                    usadas.update(re.findall(r"\bA\.(\w+)\s*\(", m["content"]))
    rep["funciones_inexistentes_en_respuestas"] = {f: n for f, n in usadas.items() if f not in existentes}
    rep["funciones_dsl_nunca_usadas"] = sorted(f for f in existentes if not f.startswith("_") and f not in usadas)

    out = os.path.join(ROOT, "DATASET", "reports", "auditoria_fugas.json")
    json.dump(rep, open(out, "w"), indent=1, ensure_ascii=False)
    for k, v in rep.items():
        print(f"\n## {k}\n{json.dumps(v, ensure_ascii=False)[:900]}")
    print("\nReporte:", out)


if __name__ == "__main__":
    main()
