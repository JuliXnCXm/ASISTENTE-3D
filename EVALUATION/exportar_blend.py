"""
exportar_blend.py
Ejecuta cada .py generado y guarda su .blend, más un .blend "galeria" con todos
los ejemplos lado a lado (una colección por ejemplo).

Uso:
  blender -b --factory-startup -P EVALUATION/exportar_blend.py -- EVALUATION/generalizacion_v2 [--patron gen_]
Salida: <dir>/blend/<nombre>.blend y <dir>/blend/galeria.blend
"""
import bpy, os, sys, glob, argparse, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "DSL", "blender"))

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("--patron", default="")
ap.add_argument("--sep", type=float, default=15.0, help="separación (m) entre ejemplos en la galería")
args = ap.parse_args(argv)

out_dir = os.path.join(os.path.abspath(args.dir), "blend")
os.makedirs(out_dir, exist_ok=True)
hechos = []
for py in sorted(glob.glob(os.path.join(args.dir, f"{args.patron}*.py"))):
    nombre = os.path.splitext(os.path.basename(py))[0].replace("__lora", "")
    try:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        for m in [m for m in sys.modules if m.startswith("blender_arch")]:
            del sys.modules[m]
        exec(compile(open(py, encoding="utf-8").read(), py, "exec"), {"__name__": "__main__"})
        dst = os.path.join(out_dir, nombre + ".blend")
        bpy.ops.wm.save_as_mainfile(filepath=dst)
        hechos.append((nombre, dst))
        print(f"BLEND_OK {nombre}", flush=True)
    except Exception as e:
        print(f"BLEND_ERR {nombre}: {type(e).__name__}: {e}", flush=True)

# Galería: anexar los objetos de cada .blend en su propia colección, en fila
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
x = 0.0
for nombre, path in hechos:
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in src.objects]
    objs = [o for o in dst.objects if o is not None and o.type not in ("CAMERA", "LIGHT")]
    col = bpy.data.collections.new(nombre)
    scene.collection.children.link(col)
    for o in objs:
        col.objects.link(o)
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ v.co for o in objs if o.type == "MESH" for v in o.data.vertices]
    if not pts:
        continue
    minx = min(p.x for p in pts); maxx = max(p.x for p in pts)
    miny = min(p.y for p in pts)
    dx, dy = x - minx, -miny
    for o in objs:
        if o.parent is None:
            o.location.x += dx
            o.location.y += dy
    x += (maxx - minx) + args.sep

sun = bpy.data.objects.new("Sol", bpy.data.lights.new("Sol", "SUN"))
sun.data.energy = 3.0
sun.rotation_euler = (math.radians(50), 0, math.radians(-35))
scene.collection.objects.link(sun)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out_dir, "galeria.blend"))
print("GALERIA_OK", len(hechos), flush=True)
