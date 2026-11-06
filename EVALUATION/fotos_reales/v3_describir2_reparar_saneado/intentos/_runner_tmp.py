DSL_PATH='/home/juliandev/Desktop/PROGRAMACION_Y_DISEÑO/MISIS/5TO_SEMESTRE/TESIS_1/ASISTENTE-3D/DSL/blender'
CODE_PATH='/home/juliandev/Desktop/PROGRAMACION_Y_DISEÑO/MISIS/5TO_SEMESTRE/TESIS_1/ASISTENTE-3D/EVALUATION/fotos_reales/v3_describir2_reparar_saneado/intentos/foto_rascacielos__lora_i1.py'
PNG_PATH='/home/juliandev/Desktop/PROGRAMACION_Y_DISEÑO/MISIS/5TO_SEMESTRE/TESIS_1/ASISTENTE-3D/EVALUATION/fotos_reales/v3_describir2_reparar_saneado/intentos/foto_rascacielos__lora_i1.png'
JSON_PATH='/home/juliandev/Desktop/PROGRAMACION_Y_DISEÑO/MISIS/5TO_SEMESTRE/TESIS_1/ASISTENTE-3D/EVALUATION/fotos_reales/v3_describir2_reparar_saneado/intentos/foto_rascacielos__lora_i1.eval.json'

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
