# generate_multimodal_assets.py
# ---------------------------------------------------------------------------
# Genera, en UN SOLO render y desde la MISMA cámara (alineados píxel a píxel):
#   <pid>_rgb.png        render RGB
#   <pid>_depth.exr      profundidad métrica REAL (pase Z, metros, 1 canal float32)
#   <pid>_depth.png      visualización 8-bit de la profundidad (claro = cerca)
#   <pid>_camera.json    intrínsecos K, extrínsecos (cam_to_world / world_to_cam)
#
# Reemplaza a generate_metric_depth.py, que en Blender >= 4 guardaba el render
# RGB como "_depth.exr" (scene.node_tree ya no existe) y escribía la cámara
# antes de actualizar matrix_world (matriz identidad).
#
# Uso (Blender 4.2+ / 5.x):
#   blender -b --factory-startup -P DATASET/scripts/generate_multimodal_assets.py -- \
#       --dataset DATASET/dataset_creation_v1.json [--ids p0001 p0002] \
#       [--shard 0 --num-shards 4] [--skip-existing] [--res 768 768]
# Para escenas sin .blend (p.ej. p5000+) usa --build-missing: ejecuta el código
# del ítem con el DSL y guarda el .blend antes de renderizar.
# ---------------------------------------------------------------------------
import bpy
import os
import sys
import json
import math
import argparse
import traceback
from mathutils import Vector, Matrix

GENERATOR_VERSION = "2.1"
HERE = os.path.dirname(os.path.abspath(__file__))
DSL_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "DSL", "blender"))


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--ids", nargs="*", default=None)
    ap.add_argument("--res", nargs=2, type=int, default=[768, 768])
    ap.add_argument("--skip-existing", action="store_true",
                    help="saltar escenas ya generadas con esta versión del generador")
    ap.add_argument("--build-missing", action="store_true",
                    help="crear el .blend desde el código si no existe")
    ap.add_argument("--rebuild", action="store_true",
                    help="reconstruir SIEMPRE el .blend desde python_code con el DSL actual (imagen = código)")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--num-shards", type=int, default=1)
    ap.add_argument("--report", default=None, help="JSONL con el resultado por escena")
    return ap.parse_args(argv)


# ── Geometría de encuadre ───────────────────────────────────────────────────
TERRAIN_KEYWORDS = ("terreno", "suelo", "ground", "cesped", "césped",
                    "plano", "terrain", "grass", "land")
GEOM_TYPES = {"MESH", "CURVE", "SURFACE", "META", "FONT"}


def is_terrain_object(ob):
    name = ob.name.lower()
    pts = [ob.matrix_world @ Vector(p) for p in ob.bound_box]
    sx = max(p.x for p in pts) - min(p.x for p in pts)
    sy = max(p.y for p in pts) - min(p.y for p in pts)
    sz = max(p.z for p in pts) - min(p.z for p in pts)
    max_xy = max(sx, sy, 0.001)
    if any(kw in name for kw in TERRAIN_KEYWORDS):
        return True
    return max_xy > 15.0 and (sz / max_xy) < 0.05


def bbox_world(objs, exclude_terrain=True):
    mins = Vector((math.inf,) * 3)
    maxs = Vector((-math.inf,) * 3)
    ok = False
    for ob in objs:
        if ob.type not in GEOM_TYPES or not ob.visible_get():
            continue
        if exclude_terrain and is_terrain_object(ob):
            continue
        ok = True
        for p in ob.bound_box:
            w = ob.matrix_world @ Vector(p)
            mins = Vector((min(mins.x, w.x), min(mins.y, w.y), min(mins.z, w.z)))
            maxs = Vector((max(maxs.x, w.x), max(maxs.y, w.y), max(maxs.z, w.z)))
    if not ok:
        if exclude_terrain:
            return bbox_world(objs, exclude_terrain=False)
        return Vector((-0.5, -0.5, 0.0)), Vector((0.5, 0.5, 1.0))
    return mins, maxs


def look_at(cam_obj, target):
    d = target - cam_obj.location
    cam_obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def intrinsics(cam, res_x, res_y):
    """K en píxeles. Fuerza sensor_fit HORIZONTAL para que sea inequívoco."""
    f_px = cam.data.lens * res_x / cam.data.sensor_width
    return [[f_px, 0.0, res_x / 2.0], [0.0, f_px, res_y / 2.0], [0.0, 0.0, 1.0]]


def setup_camera_and_light(scene, res_x, res_y):
    for ob in [o for o in scene.objects if o.type in ('CAMERA', 'LIGHT')]:
        bpy.data.objects.remove(ob, do_unlink=True)

    cam = bpy.data.objects.new("RenderCam", bpy.data.cameras.new("RenderCam"))
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.data.lens = 35.0
    cam.data.sensor_fit = 'HORIZONTAL'
    cam.data.sensor_width = 36.0
    cam.data.clip_start = 0.01
    cam.data.clip_end = 10000.0

    mins, maxs = bbox_world(list(scene.objects))
    center = (mins + maxs) * 0.5
    size = maxs - mins
    max_dim = max(size.x, size.y, size.z, 0.001)

    # Distancia para que la esfera envolvente quepa en el FOV horizontal
    # (imagen cuadrada → FOV horizontal = vertical).
    fov = 2.0 * math.atan((cam.data.sensor_width / 2.0) / cam.data.lens)
    radius = 0.5 * size.length
    dist = max(radius / math.sin(fov / 2.0) * 1.02, 0.5)
    az, el = math.radians(45.0), math.radians(30.0)
    cam.location = center + Vector((dist * math.cos(el) * math.sin(az),
                                    -dist * math.cos(el) * math.cos(az),
                                    dist * math.sin(el)))
    look_at(cam, center)

    key = bpy.data.objects.new("KeyLight", bpy.data.lights.new("KeyLight", 'SUN'))
    key.data.energy = 2.8
    key.data.angle = math.radians(8)
    key.rotation_euler = (math.radians(50), 0.0, math.radians(-35))
    scene.collection.objects.link(key)
    fill = bpy.data.objects.new("FillLight", bpy.data.lights.new("FillLight", 'SUN'))
    fill.data.energy = 0.6
    fill.rotation_euler = (math.radians(65), 0.0, math.radians(150))
    scene.collection.objects.link(fill)

    # IMPORTANTE: actualizar matrices antes de leer matrix_world
    bpy.context.view_layer.update()
    return cam, center, max_dim


def setup_world(scene):
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    try:
        world.use_nodes = True
        bg = world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs[0].default_value = (0.35, 0.42, 0.55, 1.0)
            bg.inputs[1].default_value = 0.18
    except Exception:
        world.color = (0.62, 0.66, 0.72)


def setup_render(scene, res_x, res_y):
    scene.render.engine = 'BLENDER_EEVEE' if 'BLENDER_EEVEE' in {
        e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items} else 'BLENDER_EEVEE_NEXT'
    try:
        scene.eevee.taa_render_samples = 16
    except Exception:
        pass
    scene.render.resolution_x, scene.render.resolution_y = res_x, res_y
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'AgX' if 'AgX' in [e.identifier for e in scene.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
    scene.view_layers[0].use_pass_z = True
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'


def setup_depth_output(scene, out_dir, stem):
    """Compositor: RenderLayers.Depth → File Output EXR float32 (1 canal)."""
    if hasattr(scene, "compositing_node_group"):          # Blender ≥ 5.0
        tree = bpy.data.node_groups.new("DepthComp", "CompositorNodeTree")
        scene.compositing_node_group = tree
    else:                                                 # Blender 4.x
        scene.use_nodes = True
        tree = scene.node_tree
        tree.nodes.clear()
    rl = tree.nodes.new("CompositorNodeRLayers")
    fo = tree.nodes.new("CompositorNodeOutputFile")
    if hasattr(fo.format, "media_type"):                  # Blender ≥ 5.0
        fo.format.media_type = 'IMAGE'
    fo.format.file_format = 'OPEN_EXR'
    fo.format.color_depth = '32'
    # RGB con 3 canales iguales: OpenCV no lee EXR de 1 canal ('V') que escribe Blender
    fo.format.color_mode = 'RGB'
    try:
        fo.format.exr_codec = 'ZIP'   # sin pérdida
    except Exception:
        pass
    if hasattr(fo, "file_output_items"):                  # API 5.x
        fo.directory = out_dir
        fo.file_name = ""
        fo.file_output_items.clear()
        fo.file_output_items.new('FLOAT', f"{stem}_depthraw")
        target_socket = fo.inputs[0]
    else:                                                 # API 4.x
        fo.base_path = out_dir
        fo.file_slots[0].path = f"{stem}_depthraw"
        target_socket = fo.inputs[0]
    depth_socket = rl.outputs.get("Depth")
    if depth_socket is None:
        raise RuntimeError("El nodo Render Layers no expone 'Depth' (use_pass_z)")
    tree.links.new(depth_socket, target_socket)
    # Blender 5: la salida del compositor necesita un Group Output para ejecutarse
    if hasattr(scene, "compositing_node_group"):
        try:
            tree.interface.new_socket("Image", in_out='OUTPUT', socket_type='NodeSocketColor')
            go = tree.nodes.new("NodeGroupOutput")
            tree.links.new(rl.outputs["Image"], go.inputs[0])
        except Exception:
            pass


def find_and_rename(out_dir, stem, final_path):
    cands = [f for f in os.listdir(out_dir) if f.startswith(f"{stem}_depthraw") and f.endswith(".exr")]
    if not cands:
        return False
    cands.sort(key=lambda f: os.path.getmtime(os.path.join(out_dir, f)), reverse=True)
    if os.path.exists(final_path):
        os.remove(final_path)
    os.rename(os.path.join(out_dir, cands[0]), final_path)
    for f in cands[1:]:
        os.remove(os.path.join(out_dir, f))
    return True


def depth_preview_png(exr_path, png_path):
    """Lee el EXR con Blender y escribe una vista 8-bit (claro = cerca)."""
    img = bpy.data.images.load(exr_path, check_existing=False)
    w, h = img.size
    px = list(img.pixels[:])
    ch = img.channels
    vals = px[0::ch]
    finite = [v for v in vals if 0 < v < 1e4]
    stats = {"valid_frac": len(finite) / max(1, len(vals))}
    if finite:
        lo, hi = min(finite), max(finite)
        stats.update(min=lo, max=hi)
        rng = max(hi - lo, 1e-6)
        out = []
        for v in vals:
            g = 1.0 - (v - lo) / rng if 0 < v < 1e4 else 0.0
            out += [g, g, g, 1.0]
        prev = bpy.data.images.new("depth_prev", w, h, alpha=True)
        prev.pixels[:] = out
        prev.filepath_raw = png_path
        prev.file_format = 'PNG'
        prev.save()
        bpy.data.images.remove(prev)
    bpy.data.images.remove(img)
    return stats


def save_camera_meta(scene, cam, res_x, res_y, path, center, max_dim):
    bpy.context.view_layer.update()
    c2w = cam.matrix_world.copy()
    meta = {
        "generator_version": GENERATOR_VERSION,
        "camera_type": "perspective",
        "convention": "Blender: cámara mira -Z, +Y arriba; depth.exr = profundidad Z en metros (pase Z, 3 canales iguales, fondo = valor enorme)",
        "resolution": [res_x, res_y],
        "intrinsics": intrinsics(cam, res_x, res_y),
        "extrinsics_world_to_cam": [list(r) for r in c2w.inverted()],
        "cam_to_world": [list(r) for r in c2w],
        "location": list(cam.location),
        "focal_length_mm": cam.data.lens,
        "sensor_width_mm": cam.data.sensor_width,
        "sensor_fit": cam.data.sensor_fit,
        "clip_start": cam.data.clip_start,
        "clip_end": cam.data.clip_end,
        "scene_center": list(center),
        "scene_max_dim": max_dim,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


def build_blend_from_code(item, blend_path):
    if DSL_DIR not in sys.path:
        sys.path.insert(0, DSL_DIR)
    import importlib
    import blender_arch as A
    importlib.reload(A)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    code = item.get("python_code") or item.get("code") or ""
    if not code.strip():
        raise RuntimeError("item sin python_code")
    g = {"__name__": "__main__"}
    exec(compile(code, f"<{item.get('id')}>", "exec"), g)
    os.makedirs(os.path.dirname(blend_path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)


def process_item(pid, item, dataset_dir, res, build_missing, rebuild=False):
    rel_blend = item.get("blend_path") or f"out_assets/{pid}/{pid}.blend"
    abs_blend = os.path.join(dataset_dir, rel_blend)
    aviso = None
    if rebuild or not os.path.exists(abs_blend):
        if not (rebuild or build_missing):
            return {"id": pid, "ok": False, "error": "sin .blend"}
        tmp = abs_blend[:-6] + "__new.blend"
        try:
            build_blend_from_code(item, tmp)
            os.replace(tmp, abs_blend)
        except Exception as e:
            if os.path.exists(tmp):
                os.remove(tmp)
            if not os.path.exists(abs_blend):
                raise
            aviso = f"rebuild falló, se usa .blend previo: {type(e).__name__}: {e}"[:300]
    out_dir = os.path.dirname(abs_blend)
    paths = {k: os.path.join(out_dir, f"{pid}_{k}") for k in
             ("rgb.png", "depth.exr", "depth.png", "camera.json")}

    bpy.ops.wm.open_mainfile(filepath=abs_blend)
    scene = bpy.context.scene
    setup_render(scene, *res)
    setup_world(scene)
    cam, center, max_dim = setup_camera_and_light(scene, *res)
    setup_depth_output(scene, out_dir, pid)

    scene.render.filepath = paths["rgb.png"]
    bpy.ops.render.render(write_still=True)

    if not find_and_rename(out_dir, pid, paths["depth.exr"]):
        return {"id": pid, "ok": False, "error": "no se generó el EXR de profundidad"}
    stats = depth_preview_png(paths["depth.exr"], paths["depth.png"])
    save_camera_meta(scene, cam, res[0], res[1], paths["camera.json"], center, max_dim)

    rel = lambda p: os.path.relpath(p, dataset_dir).replace("\\", "/")
    return {"id": pid, "ok": stats.get("valid_frac", 0) > 0.005, "aviso": aviso,
            "reconstruido": bool(rebuild or build_missing) and aviso is None,
            "blend_path": rel(abs_blend),
            "render_path": rel(paths["rgb.png"]),
            "depth_path": rel(paths["depth.png"]),
            "metric_depth_path": rel(paths["depth.exr"]),
            "camera_meta_path": rel(paths["camera.json"]),
            "depth_stats": stats,
            "error": None if stats.get("valid_frac", 0) > 0.005 else "profundidad vacía"}


def ya_generado(dataset_dir, pid):
    p = os.path.join(dataset_dir, "out_assets", pid, f"{pid}_camera.json")
    try:
        return json.load(open(p)).get("generator_version") == GENERATOR_VERSION
    except Exception:
        return False


def main():
    args = parse_args()
    data = json.load(open(args.dataset, encoding="utf-8"))
    items = data.get("items", {})
    dataset_dir = os.path.dirname(os.path.abspath(args.dataset))
    ids = args.ids or sorted(items.keys())
    ids = [p for i, p in enumerate(ids) if i % args.num_shards == args.shard]
    report = open(args.report, "a") if args.report else None

    for n, pid in enumerate(ids):
        item = items.get(pid)
        if not item:
            continue
        if args.skip_existing and ya_generado(dataset_dir, pid):
            continue
        try:
            item.setdefault("id", pid)
            r = process_item(pid, item, dataset_dir, args.res, args.build_missing, args.rebuild)
        except Exception as e:
            r = {"id": pid, "ok": False, "error": f"{type(e).__name__}: {e}"[:300],
                 "trace": traceback.format_exc()[-800:]}
        print(f"[{n + 1}/{len(ids)}] {pid} {'OK' if r.get('ok') else 'ERR ' + str(r.get('error'))}", flush=True)
        if report:
            report.write(json.dumps(r, ensure_ascii=False) + "\n")
            report.flush()


if __name__ == "__main__":
    main()
