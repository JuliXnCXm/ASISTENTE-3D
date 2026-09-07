# build_blends_from_dataset.py
# Construye .blend por ítem desde un dataset JSON:
# - copia python_code a <out>/<id>/<id>.py
# - ejecuta el .py en Blender (entorno seguro con import por lista blanca)
# - guarda <out>/<id>/<id>.blend
# - actualiza el JSON con items[id]["blend_path"] = ruta al .blend (relativa)
#
# Uso:
# blender -b -P build_blends_from_dataset.py -- --dataset dataset.json --out out_dir --update-json-out dataset_out.json

import bpy
import os
import re
import sys
import json
import argparse
import builtins
import math
import bmesh
from mathutils import Vector
from datetime import datetime, timezone

# ----------------------------
# CLI
# ----------------------------
def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, help="Ruta al JSON con items.{id}.python_code")
    ap.add_argument("--out", required=True, help="Directorio raíz de salida")
    ap.add_argument("--update-json-out", default=None, help="Ruta del JSON actualizado (si no se pasa, se escribe a <dataset basename>_with_blends.json en la misma carpeta)")
    ap.add_argument("--ids", nargs="*", help="Lista de IDs concretos a procesar (p.ej., p0001 p0002). Si se omite, procesa todos.")
    ap.add_argument("--skip-existing", action="store_true", help="Saltar ítems cuyo .blend ya existe")
    ap.add_argument("--pack", action="store_true", help="Empaquetar recursos en el .blend")
    ap.add_argument("--bail-on-error", action="store_true", help="Detenerse ante el primer error")
    return ap.parse_args(argv)

# ----------------------------
# Seguridad / utilidades
# ----------------------------

BANNED_SNIPPETS = [
    "bpy.ops.wm.open_mainfile",
    "bpy.ops.wm.save_mainfile",
    "pip install",
    "import requests",
    "subprocess",
    "os.system",
    "shutil.rmtree",
]

def clean_scene():
    """Escena vacía y limpia de datablocks sin uso."""
    try:
        bpy.ops.wm.read_homefile(use_empty=True)
    except Exception:
        pass
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # limpiar datablocks
    for datablock in (bpy.data.meshes, bpy.data.cameras, bpy.data.lights, bpy.data.materials,
                      bpy.data.images, bpy.data.curves, bpy.data.collections):
        for block in list(datablock):
            if hasattr(block, "users") and block.users == 0:
                try:
                    datablock.remove(block)
                except Exception:
                    pass
    # colección raíz
    if "Collection" not in bpy.data.collections:
        root = bpy.data.collections.new("Collection")
        bpy.context.scene.collection.children.link(root)

def ensure_metric_units():
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0  # 1 unidad = 1 m

DSL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
    "..", "DSL", "blender"))

def limited_exec(code_str):
    import traceback, builtins as _bi, sys as _sys

    # Asegurar que blender_arch sea importable
    if DSL_DIR not in _sys.path:
        _sys.path.insert(0, DSL_DIR)

    allowed_roots = {"bpy", "math", "mathutils", "random", "bmesh", "numpy",
                     "blender_arch"}
    real_import = _bi.__import__

    def limited_import(name, globals=None, locals=None, fromlist=(), level=0):
        root = name.split(".")[0]
        if root not in allowed_roots:
            raise ImportError(f"Module not allowed: {name}")
        return real_import(name, globals, locals, fromlist, level)

    safe_builtins = {
        "__import__": limited_import,
        "len": len, "range": range, "min": min, "max": max, "abs": abs, "print": print,
        "round": round, "pow": pow, "divmod": divmod, "chr": chr, "ord": ord,
        "float": float, "int": int, "bool": bool, "str": str, "list": list, "dict": dict, "set": set, "tuple": tuple,
        "enumerate": enumerate, "zip": zip, "sorted": sorted, "reversed": reversed,
        "sum": sum, "any": any, "all": all, "map": map, "filter": filter,
        "hasattr": hasattr, "getattr": getattr, "setattr": setattr, "delattr": delattr,
        "isinstance": isinstance, "issubclass": issubclass, "type": type, "dir": dir, "repr": repr,
    }

    # --- Compat helpers inyectados (ver §2) ---
    COMPAT = r"""
import bpy, math
try:
    import bmesh as _bm; bmesh = _bm
except Exception:
    bmesh = None

def compat_modifier_apply(obj, mod_name):
    # Evita overrides tipo {"object": obj} que provocan: "1-2 args execution context is supported"
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod_name)

def ensure_emissive_material_for(obj, name="Emisivo", color=(1,1,1,1), strength=10.0, mix_with_bsdf=False):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree; nodes = nt.nodes; links = nt.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    if mix_with_bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (0, -120)
        emi = nodes.new("ShaderNodeEmission"); emi.location = (0, 120)
        emi.inputs["Color"].default_value = color
        emi.inputs["Strength"].default_value = strength
        add = nodes.new("ShaderNodeAddShader"); add.location = (200, 0)
        links.new(bsdf.outputs["BSDF"], add.inputs[0])
        links.new(emi.outputs["Emission"], add.inputs[1])
        links.new(add.outputs["Shader"], out.inputs["Surface"])
    else:
        emi = nodes.new("ShaderNodeEmission"); emi.location = (0, 0)
        emi.inputs["Color"].default_value = color
        emi.inputs["Strength"].default_value = strength
        links.new(emi.outputs["Emission"], out.inputs["Surface"])
    if hasattr(obj.data, "materials"):
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return mat

def ensure_glass_material_for(obj, name="GlassCompat", ior=1.52, roughness=0.05, color=(1,1,1,1)):
    # Evita usar Principled.inputs["Transmission"] (ya no existe en 4.x)
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree; nodes = nt.nodes; links = nt.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    glass = nodes.new("ShaderNodeBsdfGlass"); glass.location = (0, 0)
    glass.inputs["IOR"].default_value = ior
    glass.inputs["Roughness"].default_value = roughness
    glass.inputs["Color"].default_value = color
    links.new(glass.outputs["BSDF"], out.inputs["Surface"])
    if hasattr(obj.data, "materials"):
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return mat

def bm_extrude_and_translate(bm, faces, vec=(0,0,0)):
    # Reemplazo de bmesh.ops.extrude_face_region(..., vec=...) (vec ya no es argumento válido)
    res = bmesh.ops.extrude_face_region(bm, geom=list(faces))
    verts = [e for e in res["geom"] if hasattr(e, "co")]
    bmesh.ops.translate(bm, verts=verts, vec=vec)
    return verts

def bm_create_cylinder(bm, radius=1.0, depth=1.0, segments=32):
    # Reemplazo de bmesh.ops.create_cylinder (no existe): usa create_cone con radios iguales
    return bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                                 radius1=radius, radius2=radius, depth=depth)

def add_wedge(location=(0,0,0)):
    # Reemplazo de bpy.ops.mesh.primitive_wedge_add (requiere addon "Extra Objects")
    # Creamos un prisma triangular unitario y lo dejamos listo para escalar vía .dimensions
    mesh = bpy.data.meshes.new("Wedge")
    obj = bpy.data.objects.new("Wedge", mesh)
    bpy.context.collection.objects.link(obj)
    import bmesh as _b
    bm = _b.new()
    v0 = bm.verts.new((-0.5, -0.5,  0.0))
    v1 = bm.verts.new(( 0.5, -0.5,  0.0))
    v2 = bm.verts.new((-0.5,  0.5,  0.0))
    v3 = bm.verts.new((-0.5, -0.5,  1.0))
    v4 = bm.verts.new(( 0.5, -0.5,  1.0))
    v5 = bm.verts.new((-0.5,  0.5,  1.0))
    bm.faces.new((v0, v1, v2))       # cara base triangular
    bm.faces.new((v3, v5, v4))       # cara top
    bm.faces.new((v0, v2, v5, v3))   # lado
    bm.faces.new((v0, v3, v4, v1))   # lado
    bm.faces.new((v1, v4, v5, v2))   # lado
    bm.to_mesh(mesh); bm.free()
    obj.location = location
    return obj
"""
    code_clean = code_str.replace("```", "").lstrip("\ufeff")
    for bad in BANNED_SNIPPETS:
        if bad in code_clean:
            raise RuntimeError(f"Código con operación prohibida detectada: {bad}")

    safe_globals = {"__builtins__": safe_builtins, "bpy": bpy, "math": math, "Vector": Vector}
    try:
        import bmesh as _bmesh; safe_globals["bmesh"] = _bmesh
    except Exception:
        pass
    try:
        import mathutils as _mu; safe_globals["mathutils"] = _mu
    except Exception:
        pass

    # inyecta compat helpers al principio
    code_clean = COMPAT + "\n" + code_clean

    # usa el MISMO dict para globals y locals
    exec(code_clean, safe_globals, safe_globals)

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def snapshot_object_names():
    return set(o.name_full for o in bpy.data.objects)

def move_new_objects_to_collection(asset_id, before_names):
    after_names = snapshot_object_names()
    new_names = sorted(list(after_names - before_names))
    col_name = f"Asset_{asset_id}"
    col = bpy.data.collections.get(col_name) or bpy.data.collections.new(col_name)
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    for name in new_names:
        obj = bpy.data.objects.get(name)
        if not obj:
            continue
        # desvincular de colecciones previas y vincular a la del asset
        for c in list(obj.users_collection):
            try:
                c.objects.unlink(obj)
            except Exception:
                pass
        col.objects.link(obj)
    return col_name, new_names

# ----------------------------
# Main
# ----------------------------
def main():
    args = parse_args()

    # Salidas/JSON
    with open(args.dataset, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", {})
    if not isinstance(items, dict) or not items:
        raise SystemExit("El JSON no contiene 'items' con formato válido.")

    # Subconjunto de IDs (si se pide)
    if args.ids:
        ids = [i for i in args.ids if i in items]
        if not ids:
            raise SystemExit("Ninguno de los IDs especificados está en el dataset.")
    else:
        ids = sorted(items.keys())

    # Ruta del JSON actualizado
    if args.update_json_out:
        updated_json_path = args.update_json_out
    else:
        base = os.path.splitext(os.path.basename(args.dataset))[0]
        updated_json_path = os.path.join(os.path.dirname(args.dataset), f"{base}_with_blends.json")

    os.makedirs(args.out, exist_ok=True)

    # Procesar ítems
    results = {"ok": [], "fail": []}

    for pid in ids:
        item = items[pid]
        prompt = item.get("prompt", "")
        code = item.get("python_code", "")

        id_dir = os.path.join(args.out, pid)
        os.makedirs(id_dir, exist_ok=True)
        py_path = os.path.join(id_dir, f"{pid}.py")
        blend_path = os.path.join(id_dir, f"{pid}.blend")
        log_path = os.path.join(id_dir, "run.log")

        # Saltar si ya existe y nos lo piden
        if args.skip_existing and os.path.exists(blend_path):
            # actualizar llave si no existe aún
            rel_blend = os.path.relpath(blend_path, start=os.path.dirname(updated_json_path))
            item["blend_path"] = rel_blend.replace("\\", "/")
            results["ok"].append(pid)
            continue

        # Guardar .py (copia fiel del código generado)
        write_file(py_path, code)

        # Ejecutar en escena limpia
        clean_scene()
        ensure_metric_units()

        before = snapshot_object_names()

        try:
            # ejecutar el .py
            with open(py_path, "r", encoding="utf-8") as f:
                code_str = f.read()
            limited_exec(code_str)

            # mover objetos nuevos a colección del asset
            col_name, new_objs = move_new_objects_to_collection(pid, before)

            # empaquetar (opcional)
            if args.pack:
                try:
                    bpy.ops.file.pack_all()
                except Exception:
                    pass

            # guardar .blend
            bpy.ops.wm.save_as_mainfile(filepath=blend_path, compress=True)

            # actualizar dataset con ruta relativa al JSON actualizado
            rel_blend = os.path.relpath(blend_path, start=os.path.dirname(updated_json_path))
            item["blend_path"] = rel_blend.replace("\\", "/")
            item["asset_collection"] = col_name
            item["objects"] = new_objs

            # log OK
            with open(log_path, "w", encoding="utf-8") as logf:
                logf.write("OK: script ejecutado y .blend guardado.\n")
            results["ok"].append(pid)

        except Exception as e:
            with open(log_path, "w", encoding="utf-8") as logf:
                logf.write(f"ERROR: {e}\n")
            results["fail"].append(pid)
            if args.bail_on_error:
                break

    # Guardar JSON actualizado
    data["meta"] = data.get("meta", {})
    data["meta"]["updated_at"] = datetime.now(timezone.utc).isoformat()
    data["meta"]["blend_output_root"] = os.path.abspath(args.out).replace("\\", "/")
    with open(updated_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Resumen consola
    print(f"[DONE] OK: {len(results['ok'])}, FAIL: {len(results['fail'])}")
    print(f"[JSON] Actualizado: {updated_json_path}")

if __name__ == "__main__":
    main()
