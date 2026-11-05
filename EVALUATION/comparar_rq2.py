#!/usr/bin/env python3
"""
comparar_rq2.py
Compara configuraciones (carpetas de resultados ya ejecutadas con ejecutar_en_blender.py)
contra la escena de referencia del test, por escena:

  ejecuta      : el código corre en Blender
  err_dim      : error relativo medio de las dimensiones del bbox global (dims ordenadas,
                 robusto a rotaciones de 90°) vs. la referencia
  dim_ok_20    : % de escenas con err_dim <= 20 %
  f1_categorias: F1 entre multiconjuntos de categorías DSL (muro×4, silla×6, ...)
  aislados     : piezas flotando

Uso: python3 EVALUATION/comparar_rq2.py EVALUATION/rq2/*
Salida: tabla markdown (y EVALUATION/rq2/comparacion.md si las carpetas están en rq2/)
"""
import json, os, sys, glob, statistics as st


def cargar(d):
    out = {}
    for f in glob.glob(os.path.join(d, "*.eval.json")):
        n = os.path.basename(f)[:-len(".eval.json")]
        caso, var = n.rsplit("__", 1)
        out.setdefault(caso, {})[var] = json.load(open(f))
    return out


def dims(b):
    return sorted([b[3] - b[0], b[4] - b[1], b[5] - b[2]]) if b else None


def err_dim(g, r):
    dg, dr = dims(g.get("bbox")), dims(r.get("bbox"))
    if not dg or not dr:
        return None
    return st.mean(abs(a - b) / max(b, 0.05) for a, b in zip(dg, dr))


def f1_cats(g, r):
    cg, cr = g.get("categorias") or {}, r.get("categorias") or {}
    if not cg and not cr:
        return None  # escena en bpy puro (sin categorías DSL): F1 no definido
    inter = sum(min(cg.get(k, 0), cr.get(k, 0)) for k in set(cg) | set(cr))
    p = inter / max(1, sum(cg.values()))
    rc = inter / max(1, sum(cr.values()))
    return 0.0 if p + rc == 0 else 2 * p * rc / (p + rc)


def resumir(d):
    data = cargar(d)
    filas = []
    for caso, v in sorted(data.items()):
        g, r = v.get("lora"), v.get("referencia")
        if not g or not r or not r.get("ok"):
            continue
        e = err_dim(g, r) if g.get("ok") else None
        filas.append(dict(caso=caso, ok=bool(g.get("ok")), err=e,
                          f1=f1_cats(g, r) if g.get("ok") else (0.0 if r.get("categorias") else None),
                          aislados=g.get("aislados", 0) if g.get("ok") else None))
    n = len(filas)
    errs = [f["err"] for f in filas if f["err"] is not None]
    return dict(config=os.path.basename(d.rstrip("/")), n=n,
                ejecuta=sum(f["ok"] for f in filas),
                err_dim_mediana=st.median(errs) if errs else None,
                dim_ok_20=sum(e <= 0.2 for e in errs),
                f1_categorias=st.mean([f["f1"] for f in filas if f["f1"] is not None] or [0]),
                n_f1=sum(f["f1"] is not None for f in filas),
                aislados=sum(f["aislados"] or 0 for f in filas)), filas


def main():
    dirs = [d for d in sys.argv[1:] if os.path.isdir(d)]
    res = [resumir(d) for d in dirs]
    lineas = ["| configuración | ejecuta | error dim. (mediana) | dims ≤20% | F1 categorías | piezas flotando |",
              "|---|---|---|---|---|---|"]
    for r, _ in res:
        em = r["err_dim_mediana"]
        em_txt = "—" if em is None else f"{em:.0%}"
        lineas.append(f"| {r['config']} | {r['ejecuta']}/{r['n']} | {em_txt} | "
                      f"{r['dim_ok_20']}/{r['n']} | {r['f1_categorias']:.2f} (n={r['n_f1']}) | {r['aislados']} |")
    # subconjunto pareado: escenas que ejecutan en TODAS las configuraciones
    comunes = set.intersection(*[{f["caso"] for f in fs if f["ok"]} for _, fs in res]) if res else set()
    if comunes:
        lineas += ["", f"Pareado (las {len(comunes)} escenas que ejecutan en todas las configuraciones):", "",
                   "| configuración | error dim. (mediana) | F1 categorías |", "|---|---|---|"]
        for r, fs in res:
            sel = [f for f in fs if f["caso"] in comunes]
            e = [f["err"] for f in sel if f["err"] is not None]
            f1 = [f["f1"] for f in sel if f["f1"] is not None]
            lineas.append(f"| {r['config']} | {st.median(e):.0%} | "
                          f"{(st.mean(f1) if f1 else float('nan')):.2f} (n={len(f1)}) |")
    # detalle por escena
    lineas += ["", "Detalle por escena (error dimensional; ✗ = no ejecuta):", "",
               "| escena | " + " | ".join(r["config"] for r, _ in res) + " |",
               "|---|" + "---|" * len(res)]
    casos = sorted({f["caso"] for _, fs in res for f in fs})
    idx = [{f["caso"]: f for f in fs} for _, fs in res]
    for c in casos:
        celdas = []
        for m in idx:
            f = m.get(c)
            celdas.append("—" if not f else ("✗" if not f["ok"] else
                          (f"{f['err']:.0%}" + (f" / F1 {f['f1']:.2f}" if f["f1"] is not None else "") if f["err"] is not None else "ok")))
        lineas.append(f"| {c} | " + " | ".join(celdas) + " |")
    txt = "\n".join(lineas)
    print(txt)
    if dirs and all(os.path.dirname(os.path.abspath(d)) == os.path.dirname(os.path.abspath(dirs[0])) for d in dirs):
        open(os.path.join(os.path.dirname(os.path.abspath(dirs[0])), "comparacion.md"), "w").write(txt + "\n")


if __name__ == "__main__":
    main()
