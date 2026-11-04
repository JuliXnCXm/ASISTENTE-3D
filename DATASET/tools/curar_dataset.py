#!/usr/bin/env python3
"""
curar_dataset.py — Curación automática del dataset de entrenamiento.

Ejecuta en Blender (headless, en paralelo) TODO el código de los splits
TRAINING/data/{train,validation,test}_multimodal.jsonl:
  - cada respuesta del assistant (todas las vueltas en multi-turno)
  - el código base que aparece en el mensaje de usuario de las ediciones
y mide por cada código:
  ejecuta / error, nº de mallas, bbox, piezas aisladas flotando, piezas bajo
  el suelo, mallas degeneradas, objetos duplicados superpuestos, y una huella
  geométrica (para detectar ediciones que no cambian nada).

Auto-fix: añade imports estándar faltantes (math, bpy, random, bmesh,
mathutils) y re-ejecuta. Los arreglos se aplican a los JSONL con --aplicar.

Uso:
  python3 DATASET/tools/curar_dataset.py --run            # ejecuta y genera reporte
  python3 DATASET/tools/curar_dataset.py --aplicar        # escribe JSONL curados
Salidas: DATASET/reports/curacion/{resultados.jsonl, resumen.json}
"""
import argparse, json, os, re, subprocess, sys, hashlib, collections, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "TRAINING", "data")
DSL = os.path.join(ROOT, "DSL", "blender")
OUT = os.path.join(ROOT, "DATASET", "reports", "curacion")
SPLITS = ("train", "validation", "test")
STD_MODULES = {"math": "import math", "bpy": "import bpy", "random": "import random",
               "bmesh": "import bmesh", "mathutils": "import mathutils"}

RUNNER = r'''
import sys, json, traceback, hashlib
sys.path.insert(0, DSL)
import bpy
from mathutils import Vector
import blender_arch as A

def medir():
    bpy.context.view_layer.update()
    ms = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    boxes = {}
    degenerados = 0
    for o in ms:
        p = [o.matrix_world @ Vector(c) for c in o.bound_box]
        b = [min(v.x for v in p), min(v.y for v in p), min(v.z for v in p),
             max(v.x for v in p), max(v.y for v in p), max(v.z for v in p)]
        boxes[o.name] = b
        if len(o.data.vertices) == 0 or max(b[3]-b[0], b[4]-b[1], b[5]-b[2]) < 1e-4:
            degenerados += 1
    def toca(a, c, eps=0.03):
        return all(a[i] <= c[i+3] + eps and c[i] <= a[i+3] + eps for i in range(3))
    names = list(boxes)
    # suelo de referencia = z mínima de la escena
    zmin = min((b[2] for b in boxes.values()), default=0.0)
    aislados = [n for n in names if boxes[n][2] > zmin + 0.10 and
                not any(toca(boxes[n], boxes[m]) for m in names if m != n)]
    def dist(a, c):
        g = [max(0.0, a[i] - c[i+3], c[i] - a[i+3]) for i in range(3)]
        return (g[0]**2 + g[1]**2 + g[2]**2) ** 0.5
    gaps = {n: min((dist(boxes[n], boxes[m]) for m in names if m != n), default=0.0) for n in aislados}
    # "grave": separada > 15 cm de todo, y no es la única pieza de la escena
    graves = [n for n, g in gaps.items() if g > 0.15]
    bajo = [n for n in names if boxes[n][5] < zmin - 0.01]
    firmas = collections.Counter(tuple(round(v, 3) for v in b) for b in boxes.values())
    duplicados = sum(c - 1 for c in firmas.values() if c > 1)
    allb = None
    if boxes:
        allb = [min(b[i] for b in boxes.values()) for i in range(3)] + \
               [max(b[i] for b in boxes.values()) for i in range(3, 6)]
    huella = hashlib.md5(json.dumps(sorted(tuple(round(v, 2) for v in b) for b in boxes.values())).encode()).hexdigest()
    cats = collections.Counter(o.get("arch_categoria") for o in bpy.context.scene.objects if o.get("arch_categoria"))
    return dict(n_mallas=len(ms), bbox=allb, aislados=len(aislados), ej_aislados=aislados[:4],
                flotantes_graves=len(graves), ej_graves=[(n, round(gaps[n], 2)) for n in graves[:4]],
                gap_max=round(max(gaps.values(), default=0.0), 3),
                bajo_suelo=len(bajo), degenerados=degenerados, duplicados=duplicados,
                huella=huella, categorias=dict(cats),
                n_vertices=sum(len(o.data.vertices) for o in ms))

import collections
out = open(OUT_PATH, "w")
for line in open(TASKS_PATH):
    t = json.loads(line)
    r = {"key": t["key"]}
    try:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        g = {"__name__": "__main__"}
        exec(compile(t["code"], "<code>", "exec"), g)
        r["ok"] = True
    except BaseException as e:
        tb = traceback.format_exc().strip().splitlines()
        r["ok"] = False
        r["error"] = (tb[-1] if tb else repr(e))[:240]
    try:
        r.update(medir())
    except BaseException as e:
        r["error_medir"] = repr(e)[:200]
    out.write(json.dumps(r) + "\n"); out.flush()
'''


def leer_jsonl(path):
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


def limpiar(code):
    m = re.search(r"```(?:python)?\s*(.*?)```", code, re.DOTALL)
    return m.group(1) if m else code


def codigo_base_de_user(text):
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return m.group(1) if m else None


def arreglar_imports(code):
    """Añade imports estándar que se usan pero no se importan. Devuelve (code, añadidos)."""
    faltan = []
    for mod, stmt in STD_MODULES.items():
        usa = re.search(rf"(?<![\w.]){mod}\.", code)
        importado = re.search(rf"^\s*(import\s+{mod}\b|from\s+{mod}\b|import\s+[\w, ]*\b{mod}\b)", code, re.M)
        if usa and not importado:
            faltan.append(stmt)
    if not faltan:
        return code, []
    lines = code.splitlines()
    # insertar tras el último import inicial
    idx = 0
    for i, l in enumerate(lines):
        if l.startswith(("import ", "from ")):
            idx = i + 1
        elif l.strip() and not l.startswith("#") and idx:
            break
    lines[idx:idx] = faltan
    return "\n".join(lines) + ("\n" if code.endswith("\n") else ""), faltan


def recolectar():
    tareas = []
    for s in SPLITS:
        for r in leer_jsonl(os.path.join(DATA, f"{s}_multimodal.jsonl")):
            turno = 0
            for mi, m in enumerate(r["messages"]):
                if m["role"] == "assistant":
                    tareas.append(dict(key=f"{s}|{r['id']}|a{mi}", split=s, id=r["id"], task=r["task_type"],
                                       msg=mi, rol="assistant", turno=turno, code=limpiar(m["content"])))
                    turno += 1
                elif m["role"] == "user" and r["task_type"] != "creation":
                    base = codigo_base_de_user(m["content"])
                    if base:
                        tareas.append(dict(key=f"{s}|{r['id']}|u{mi}", split=s, id=r["id"], task=r["task_type"],
                                           msg=mi, rol="base", turno=turno, code=base))
    return tareas


def ejecutar(tareas, blender, n_proc, tag):
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="curar_", dir=OUT)
    procs, outs = [], []
    for k in range(n_proc):
        tp, op = os.path.join(tmp, f"t{k}.jsonl"), os.path.join(tmp, f"o{k}.jsonl")
        with open(tp, "w") as f:
            for t in tareas[k::n_proc]:
                f.write(json.dumps({"key": t["key"], "code": t["code"]}) + "\n")
        rp = os.path.join(tmp, f"runner{k}.py")
        open(rp, "w").write(f"DSL={DSL!r}\nTASKS_PATH={tp!r}\nOUT_PATH={op!r}\n" + RUNNER)
        procs.append(subprocess.Popen([blender, "-b", "--factory-startup", "-P", rp],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=tmp))
        outs.append(op)
    for p in procs:
        p.wait()
    res = {}
    for op in outs:
        if os.path.exists(op):
            for l in open(op):
                r = json.loads(l)
                res[r["key"]] = r
    faltantes = [t for t in tareas if t["key"] not in res]
    if faltantes:
        print(f"[{tag}] {len(faltantes)} tareas sin resultado (crash de Blender); se reintentan una a una")
        for t in faltantes:
            r = ejecutar_una(t, blender, tmp)
            res[t["key"]] = r
    return res


def ejecutar_una(t, blender, tmp):
    tp, op = os.path.join(tmp, "uno_t.jsonl"), os.path.join(tmp, "uno_o.jsonl")
    open(tp, "w").write(json.dumps({"key": t["key"], "code": t["code"]}) + "\n")
    rp = os.path.join(tmp, "runner_uno.py")
    open(rp, "w").write(f"DSL={DSL!r}\nTASKS_PATH={tp!r}\nOUT_PATH={op!r}\n" + RUNNER)
    if os.path.exists(op):
        os.remove(op)
    try:
        subprocess.run([blender, "-b", "--factory-startup", "-P", rp], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, cwd=tmp, timeout=240)
    except subprocess.TimeoutExpired:
        return {"key": t["key"], "ok": False, "error": "timeout"}
    if os.path.exists(op) and os.path.getsize(op):
        return json.loads(open(op).readline())
    return {"key": t["key"], "ok": False, "error": "crash de Blender"}


def clasificar(t, r):
    """Devuelve (veredicto, motivos). veredicto: ok | revisar | descartar"""
    motivos = []
    if not r.get("ok"):
        return "descartar", [f"no ejecuta: {r.get('error')}"]
    if r.get("n_mallas", 0) == 0:
        return "descartar", ["escena vacía"]
    bb = r.get("bbox")
    if bb:
        dim = max(bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2])
        if dim > 2000:
            return "descartar", [f"escena gigante ({dim:.0f} m): objeto mal escalado"]
        if dim < 0.05:
            motivos.append(f"escena diminuta ({dim:.3f} m)")
    if r.get("flotantes_graves", 0):
        return "descartar", [f"{r['flotantes_graves']} pieza(s) flotando a >15 cm de todo "
                             f"(máx {r.get('gap_max', 0):.2f} m): {r.get('ej_graves')}"]
    if r.get("aislados", 0):
        motivos.append(f"{r['aislados']} pieza(s) sueltas a <15 cm (contacto impreciso)")
    if r.get("bajo_suelo", 0):
        motivos.append(f"{r['bajo_suelo']} pieza(s) bajo el suelo")
    if r.get("degenerados", 0):
        motivos.append(f"{r['degenerados']} malla(s) degenerada(s)")
    if r.get("duplicados", 0) >= 3:
        motivos.append(f"{r['duplicados']} objetos duplicados superpuestos")
    return ("revisar" if motivos else "ok"), motivos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--blender", default="/snap/bin/blender")
    ap.add_argument("--procs", type=int, default=12)
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    res_path = os.path.join(OUT, "resultados.jsonl")

    if args.run:
        tareas = recolectar()
        print(f"{len(tareas)} códigos a ejecutar")
        res = ejecutar(tareas, args.blender, args.procs, "pasada 1")
        # auto-fix de imports y segunda pasada
        refix = []
        for t in tareas:
            r = res[t["key"]]
            if not r.get("ok") and "NameError" in (r.get("error") or ""):
                code2, add = arreglar_imports(t["code"])
                if add:
                    refix.append(dict(t, code=code2, fix=add))
        if refix:
            print(f"Auto-fix de imports en {len(refix)} códigos; re-ejecutando")
            res2 = ejecutar(refix, args.blender, min(args.procs, len(refix)), "pasada fix")
            for t in refix:
                r2 = res2[t["key"]]
                r2["fix_imports"] = t["fix"]
                r2["code_fixed"] = t["code"]
                res[t["key"]] = r2
        # edición sin efecto: huella del resultado == huella del código base
        bases = {}
        for t in tareas:
            if t["rol"] == "base":
                bases[(t["split"], t["id"], t["turno"])] = res[t["key"]].get("huella")
        with open(res_path, "w") as f:
            for t in tareas:
                r = res[t["key"]]
                ver, mot = clasificar(t, r)
                if t["rol"] == "assistant" and t["task"] != "creation":
                    hb = bases.get((t["split"], t["id"], t["turno"]))
                    if hb and r.get("ok") and r.get("huella") == hb:
                        mot.append("edición sin efecto geométrico (resultado == base)")
                        ver = "revisar" if ver == "ok" else ver
                f.write(json.dumps({**{k: v for k, v in t.items() if k != "code"}, **r,
                                    "veredicto": ver, "motivos": mot}, ensure_ascii=False) + "\n")
        resumir(res_path)

    if args.aplicar:
        aplicar(res_path)


def resumir(res_path):
    R = [json.loads(l) for l in open(res_path)]
    resumen = {"codigos": len(R),
               "por_veredicto": dict(collections.Counter(r["veredicto"] for r in R)),
               "por_rol": {f"{a}:{b}": c for (a, b), c in
                           collections.Counter((r["rol"], r["veredicto"]) for r in R).items()},
               "imports_arreglados": sum(bool(r.get("fix_imports")) and r.get("ok") for r in R),
               "motivos": dict(collections.Counter(re.sub(r"^\d+ ", "N ", m.split(":")[0])
                                                   for r in R for m in r["motivos"]).most_common()),
               "errores": dict(collections.Counter((r.get("error") or "")[:110] for r in R
                                                   if not r.get("ok")).most_common(25))}
    json.dump(resumen, open(os.path.join(OUT, "resumen.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(resumen, ensure_ascii=False, indent=1))


def aplicar(res_path):
    """Escribe los JSONL curados:
       - aplica arreglos de imports en el código (assistant y código base del user)
       - elimina ejemplos con algún código del assistant que no ejecuta o escena vacía
       - elimina ejemplos marcados en DATASET/reports/curacion/descartes_manuales.json
       Los originales quedan en git."""
    R = {json.loads(l)["key"]: json.loads(l) for l in open(res_path)}
    manual_path = os.path.join(OUT, "descartes_manuales.json")
    manual = json.load(open(manual_path)) if os.path.exists(manual_path) else {}
    log = collections.Counter()
    for s in SPLITS:
        p = os.path.join(DATA, f"{s}_multimodal.jsonl")
        rows, keep = leer_jsonl(p), []
        for r in rows:
            descartar = False
            for mi, m in enumerate(r["messages"]):
                key = f"{s}|{r['id']}|{'a' if m['role'] == 'assistant' else 'u'}{mi}"
                res = R.get(key)
                if not res:
                    continue
                if res.get("fix_imports") and res.get("ok"):
                    if m["role"] == "assistant":
                        m["content"] = res["code_fixed"]
                    else:
                        old = codigo_base_de_user(m["content"])
                        m["content"] = m["content"].replace(old, res["code_fixed"])
                    log[f"{s}:imports_arreglados"] += 1
                if m["role"] == "assistant" and res["veredicto"] == "descartar":
                    descartar = True
            if r["id"] in manual.get(s, []) or r["id"] in manual.get("*", []):
                descartar = True
                log[f"{s}:descarte_manual"] += 1
            if descartar:
                log[f"{s}:descartados"] += 1
            else:
                keep.append(r)
        with open(p, "w", encoding="utf-8") as f:
            for r in keep:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        log[f"{s}:final"] = len(keep)
        log[f"{s}:original"] = len(rows)
    print(dict(log))
    json.dump(dict(log), open(os.path.join(OUT, "aplicado.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
