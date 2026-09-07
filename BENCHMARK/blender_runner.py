# blender_runner.py
import bpy, bmesh, json, sys, os, argparse, traceback

def validate_scene():
    mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    total_v = total_e = total_f = 0
    non_manifold = zero_area = 0
    for o in mesh_objs:
        me = o.data
        me.validate(verbose=False); me.update()
        total_v += len(me.vertices); total_e += len(me.edges); total_f += len(me.polygons)
        bm = bmesh.new(); bm.from_mesh(me)
        non_manifold += sum(1 for e in bm.edges if not e.is_manifold)
        zero_area += sum(1 for f in bm.faces if f.calc_area() <= 1e-12)
        bm.free()
    return {
        "mesh_objects": len(mesh_objs),
        "total_vertices": total_v,
        "total_edges": total_e,
        "total_faces": total_f,
        "non_manifold_edges": non_manifold,
        "zero_area_faces": zero_area
    }

def run_script(path):
    code = open(path, "r", encoding="utf-8").read()
    # Intento opcional de inyectar blender_arch si el benchmark lo indicó
    arch_dir = os.environ.get("ARCH_DIR_HINT", "")
    if arch_dir and os.path.isdir(arch_dir) and arch_dir not in sys.path:
        sys.path.insert(0, arch_dir)
    g = {"__name__": "__main__"}
    try:
        import blender_arch as A  # si existe, queda disponible para el código del modelo
        g["A"] = A
    except Exception:
        pass
    exec(compile(code, path, "exec"), g, g)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=False)
    ap.add_argument("--report", required=True)
    args = ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])

    bpy.ops.wm.read_factory_settings(use_empty=True)

    report = {"notes": ""}
    try:
        run_script(args.script)
        report.update(validate_scene())
        report["notes"] = "ok"
    except Exception as e:
        report.update(validate_scene())
        report["notes"] = f"runtime_error: {e}"
        traceback.print_exc()

    out = args.out or os.environ.get("BLEND_OUT", "")
    if out:
        try:
            bpy.ops.wm.save_as_mainfile(filepath=out)
        except Exception as e:
            report["notes"] += f" | save_error: {e}"

    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()

