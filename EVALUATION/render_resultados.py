"""
render_resultados.py
Render "bonito" (EEVEE, misma iluminación/cámara que el dataset, vista de corte en
interiores) de cada .py generado en una carpeta de resultados.

Uso:
  blender -b --factory-startup -P EVALUATION/render_resultados.py -- EVALUATION/generalizacion_v2 [--patron gen_] [--res 900]
Salida: <dir>/<nombre>_render.png
"""
import bpy, os, sys, glob, argparse, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "DSL", "blender"))
sys.path.insert(0, os.path.join(ROOT, "DATASET", "scripts"))
import generate_multimodal_assets as G  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("--patron", default="")
ap.add_argument("--res", type=int, default=900)
args = ap.parse_args(argv)

for py in sorted(glob.glob(os.path.join(args.dir, f"{args.patron}*.py"))):
    nombre = os.path.splitext(os.path.basename(py))[0]
    out = os.path.join(os.path.abspath(args.dir), f"{nombre}_render.png")
    try:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        for m in [m for m in sys.modules if m.startswith("blender_arch")]:
            del sys.modules[m]
        code = open(py, encoding="utf-8").read()
        exec(compile(code, py, "exec"), {"__name__": "__main__"})
        scene = bpy.context.scene
        G.setup_render(scene, args.res, args.res)
        scene.view_layers[0].use_pass_z = False
        G.setup_world(scene)
        corte = G.ocultar_techos_si_interior(scene)
        G.setup_camera_and_light(scene, args.res, args.res, elevacion=55.0 if corte else 30.0)
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print(f"RENDER_OK {nombre} corte={corte}", flush=True)

        # Edificios con columnas: segunda vista sin fachada para ver la estructura
        geoms = [o for o in scene.objects if o.type in G.GEOM_TYPES]
        info = [(o, *G._categorias_ancestros(o)) for o in geoms]
        if any("columna" in cats or any("columna" in n.lower() for n in names) for _, cats, names in info):
            claves = ("vidrio", "cortina", "fachada", "muro", "ventana", "parteluz", "mullion")
            for o, cats, names in info:
                if cats & {"muro", "ventana"} or any(k in n.lower() for n in names[:2] for k in claves):
                    o.hide_render = True
            scene.render.filepath = out.replace("_render.png", "_estructura.png")
            bpy.ops.render.render(write_still=True)
            print(f"RENDER_OK {nombre} estructura", flush=True)
    except Exception as e:
        print(f"RENDER_ERR {nombre}: {type(e).__name__}: {e}", flush=True)
        traceback.print_exc()
