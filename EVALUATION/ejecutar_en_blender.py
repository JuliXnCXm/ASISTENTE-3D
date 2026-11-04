#!/usr/bin/env python3
"""
ejecutar_en_blender.py
Ejecuta cada .py generado en un proceso Blender aislado (headless), mide
ejecutabilidad + métricas geométricas simples y hace un render Workbench.

Uso:
  python3 EVALUATION/ejecutar_en_blender.py EVALUATION/resultados_local [--blender /snap/bin/blender]
Salida: <dir>/evaluacion.json, <dir>/<nombre>.png, <dir>/resumen.md
"""
import json, os, subprocess, sys, glob, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DSL = os.path.join(os.path.dirname(HERE), "DSL", "blender")

RUNNER = r'''
import sys, json, traceback, math
sys.path.insert(0, DSL_PATH)
import bpy
from mathutils import Vector
res = {"ok": False, "error": None}
try:
    code = open(CODE_PATH, encoding="utf-8").read()
    g = {"__name__": "__main__"}
    exec(compile(code, CODE_PATH, "exec"), g)
    res["ok"] = True
except BaseException as e:
    tb = traceback.format_exc().strip().splitlines()
    res["error"] = (tb[-1] if tb else repr(e))[:300]
    linea = [l for l in tb if CODE_PATH in l]
    res["linea"] = linea[-1].strip()[:200] if linea else None
try:
    bpy.context.view_layer.update()
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.visible_get()]
    def bb(o):
        p = [o.matrix_world @ Vector(c) for c in o.bound_box]
        return [min(v.x for v in p), min(v.y for v in p), min(v.z for v in p),
                max(v.x for v in p), max(v.y for v in p), max(v.z for v in p)]
    boxes = {o.name: bb(o) for o in meshes}
    cats = {}
    for o in bpy.context.scene.objects:
        c = o.get("arch_categoria")
        if c: cats[c] = cats.get(c, 0) + 1
    def toca(a, b, eps=0.02):
        return all(a[i] <= b[i+3] + eps and b[i] <= a[i+3] + eps for i in range(3))
    names = list(boxes)
    aislados = [n for n in names if boxes[n][2] > 0.05 and not any(toca(boxes[n], boxes[m]) for m in names if m != n)]
    bajo_suelo = [n for n in names if boxes[n][5] < -0.5]
    if boxes:
        allb = [min(b[i] for b in boxes.values()) for i in range(3)] + [max(b[i] for b in boxes.values()) for i in range(3, 6)]
    else:
        allb = None
    res.update(n_meshes=len(meshes), categorias=cats, bbox=allb,
               aislados=len(aislados), ejemplos_aislados=aislados[:5], bajo_suelo=len(bajo_suelo),
               n_vertices=sum(len(o.data.vertices) for o in meshes))
    if meshes and allb:
        sc = bpy.context.scene
        for o in [o for o in sc.objects if o.type == 'CAMERA']:
            pass
        cam = bpy.data.objects.new("_EvalCam", bpy.data.cameras.new("_EvalCam"))
        sc.collection.objects.link(cam)
        c = Vector(((allb[0]+allb[3])/2, (allb[1]+allb[4])/2, (allb[2]+allb[5])/2))
        size = max(allb[3]-allb[0], allb[4]-allb[1], allb[5]-allb[2], 1.0)
        cam.location = c + Vector((1.1, -1.5, 0.9)).normalized() * size * 1.9
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
        cam.data.lens = 35
        cam.data.clip_end = size * 20
        sc.camera = cam
        sc.render.engine = 'BLENDER_WORKBENCH'
        sh = sc.display.shading
        sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'
        sh.show_shadows = True; sh.show_cavity = True
        sc.render.resolution_x, sc.render.resolution_y = 640, 520
        sc.render.filepath = PNG_PATH
        bpy.ops.render.render(write_still=True)
        res["render"] = PNG_PATH
except BaseException as e:
    res["error_metricas"] = repr(e)[:200]
open(JSON_PATH, "w").write(json.dumps(res))
'''


def evaluar(py, blender, timeout=180):
    base = py[:-3]
    out_json, png = base + ".eval.json", base + ".png"
    runner = os.path.abspath(os.path.join(os.path.dirname(py), "_runner_tmp.py"))
    with open(runner, "w") as f:
        f.write(f"DSL_PATH={DSL!r}\nCODE_PATH={os.path.abspath(py)!r}\n"
                f"PNG_PATH={os.path.abspath(png)!r}\nJSON_PATH={os.path.abspath(out_json)!r}\n" + RUNNER)
    if os.path.exists(out_json):
        os.remove(out_json)
    try:
        subprocess.run([blender, "-b", "--factory-startup", "-P", runner],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout,
                       cwd=os.path.dirname(os.path.abspath(py)))
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout {timeout}s"}
    if not os.path.exists(out_json):
        return {"ok": False, "error": "Blender terminó sin reporte (crash)"}
    return json.load(open(out_json))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--blender", default="/snap/bin/blender")
    args = ap.parse_args()
    files = sorted(f for f in glob.glob(os.path.join(args.dir, "*.py")) if not os.path.basename(f).startswith("_"))
    res = {}
    for f in files:
        n = os.path.basename(f)[:-3]
        r = evaluar(f, args.blender)
        res[n] = r
        estado = "OK " if r.get("ok") else "ERR"
        print(f"{estado} {n:45s} meshes={r.get('n_meshes', 0):4} cats={r.get('categorias', {})} "
              f"aislados={r.get('aislados', '-')} {('| ' + str(r.get('error'))) if not r.get('ok') else ''}", flush=True)
    json.dump(res, open(os.path.join(args.dir, "evaluacion.json"), "w"), ensure_ascii=False, indent=2)
    tmp = os.path.join(args.dir, "_runner_tmp.py")
    if os.path.exists(tmp):
        os.remove(tmp)

    # Resumen por variante
    lineas = ["| variante | ejecutables | total |", "|---|---|---|"]
    for var in ("lora", "base", "referencia"):
        ks = [k for k in res if k.endswith("__" + var)]
        if ks:
            ok = sum(res[k].get("ok", False) for k in ks)
            lineas.append(f"| {var} | {ok} | {len(ks)} |")
    open(os.path.join(args.dir, "resumen.md"), "w").write("\n".join(lineas) + "\n")
    print("\n".join(lineas))


if __name__ == "__main__":
    main()
