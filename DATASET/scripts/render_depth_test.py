# render_depth_test.py
# Prueba de render RGB + depth map desde .blend files.
# Genera para cada item: {pid}_rgb.png y {pid}_depth.png
#
# Uso:
#   blender -b -P render_depth_test.py -- \
#     --dataset dataset_v2_with_blends.json \
#     --out depth_test \
#     --ids p0001 p0002 p0003 p0004 p0005

import bpy
import os
import sys
import json
import math
import argparse
from mathutils import Vector, Matrix

def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ids", nargs="*", default=None)
    ap.add_argument("--res", nargs=2, type=int, default=[768, 768])
    ap.add_argument("--skip-existing", action="store_true")
    return ap.parse_args(argv)

def abs_from_rel(base_json_path, maybe_rel_path):
    if os.path.isabs(maybe_rel_path):
        return maybe_rel_path
    base_dir = os.path.dirname(os.path.abspath(base_json_path))
    return os.path.abspath(os.path.join(base_dir, maybe_rel_path))

def look_at(cam_obj, target, up=Vector((0, 0, 1))):
    loc = cam_obj.location
    forward = (target - loc).normalized()
    right = forward.cross(up).normalized()
    up2 = right.cross(forward).normalized()
    rot = Matrix((
        (right.x,  up2.x, -forward.x),
        (right.y,  up2.y, -forward.y),
        (right.z,  up2.z, -forward.z),
    ))
    cam_obj.rotation_euler = rot.to_euler()

TERRAIN_KEYWORDS = ("terreno", "suelo", "ground", "cesped", "césped",
                    "piso", "plano", "terrain", "floor", "grass", "land")

def is_terrain_object(ob):
    """Detecta terreno/suelo: plano en Z Y grande en XY (> 15m).
    Excluye losas y pisos arquitectónicos que son planos pero pequeños."""
    name = ob.name.lower()
    pts = [ob.matrix_world @ Vector(p) for p in ob.bound_box]
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    sx = max(xs) - min(xs)
    sy = max(ys) - min(ys)
    sz = max(zs) - min(zs)
    max_xy = max(sx, sy, 0.001)
    # Solo excluir si coincide nombre O si es muy grande (>15m) Y muy plano
    if any(kw in name for kw in TERRAIN_KEYWORDS):
        return True
    if max_xy > 15.0 and (sz / max_xy) < 0.05:
        return True
    return False

def compute_bbox_world(objs, exclude_terrain=False):
    types_ok = {"MESH", "CURVE", "SURFACE", "META", "FONT"}
    mins = Vector(( float('inf'),  float('inf'),  float('inf')))
    maxs = Vector((-float('inf'), -float('inf'), -float('inf')))
    any_ok = False
    for ob in objs:
        if ob.type not in types_ok:
            continue
        if exclude_terrain and is_terrain_object(ob):
            continue
        any_ok = True
        for p in ob.bound_box:
            wp = ob.matrix_world @ Vector(p)
            mins.x = min(mins.x, wp.x)
            mins.y = min(mins.y, wp.y)
            mins.z = min(mins.z, wp.z)
            maxs.x = max(maxs.x, wp.x)
            maxs.y = max(maxs.y, wp.y)
            maxs.z = max(maxs.z, wp.z)
    if not any_ok:
        return Vector((-0.5, -0.5, 0.0)), Vector((0.5, 0.5, 1.0))
    return mins, maxs

def setup_camera_and_light(item, res_x, res_y):
    scene = bpy.context.scene

    # Camara
    cam = next((ob for ob in scene.objects if ob.type == 'CAMERA'), None)
    if cam is None:
        cam_data = bpy.data.cameras.new("RenderCam")
        cam = bpy.data.objects.new("RenderCam", cam_data)
        scene.collection.objects.link(cam)
    scene.camera = cam

    cam.data.lens = 35.0
    cam.data.sensor_width = 36.0
    cam.data.sensor_height = 24.0
    cam.data.clip_start = 0.01
    cam.data.clip_end = 10000.0

    # Luz
    light = scene.objects.get("RenderKeyLight")
    if light is None:
        light_data = bpy.data.lights.new("RenderKeyLight", type='AREA')
        light = bpy.data.objects.new("RenderKeyLight", light_data)
        scene.collection.objects.link(light)
    if light.data.type != 'AREA':
        light.data.type = 'AREA'

    # Obtener objetos del asset
    col_name = item.get("asset_collection")
    objs = []
    if col_name and col_name in bpy.data.collections:
        objs = list(bpy.data.collections[col_name].objects)
    if not objs:
        objs = [o for o in scene.objects if o.type in {"MESH","CURVE","SURFACE","META","FONT"}]

    # Framing: excluir terreno para que la cámara encuadre el edificio, no el suelo
    mins, maxs = compute_bbox_world(objs, exclude_terrain=True)
    center = (mins + maxs) * 0.5
    size   = (maxs - mins)
    max_dim = max(size.x, size.y, size.z, 0.001)

    fov_v = 2.0 * math.atan((cam.data.sensor_height / 2.0) / cam.data.lens)
    half_diag = math.sqrt(size.x**2 + size.y**2 + size.z**2) * 0.5
    dist = (half_diag / math.tan(fov_v * 0.5)) * 1.25

    az = math.radians(45.0)
    el = math.radians(35.0)
    cam.location = Vector((
        center.x + dist * math.cos(el) * math.sin(az),
        center.y - dist * math.cos(el) * math.cos(az),
        center.z + dist * math.sin(el),
    ))
    look_at(cam, center)

    light.location = Vector((
        center.x - max_dim * 0.5,
        center.y - max_dim * 0.5,
        center.z + max_dim * 2.0,
    ))
    light.rotation_euler = (math.radians(-45), 0.0, math.radians(-30))
    light.data.energy = 800.0
    light.data.size = max(max_dim * 0.8, 0.5)
    if hasattr(light.data, "size_y"):
        light.data.size_y = max(max_dim * 0.8, 0.5)

    # Rango real de profundidad: distancia cámara↔bbox con margen
    depth_near = max(cam.data.clip_start, dist - half_diag * 1.5)
    depth_far  = dist + half_diag * 1.5

    return cam, depth_near, depth_far

def setup_world_bg(scene):
    """Pone fondo gris oscuro."""
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    world = scene.world
    if hasattr(world, 'node_tree') and world.node_tree:
        nt = world.node_tree
        bg = nt.nodes.get("Background") or nt.nodes.new("ShaderNodeBackground")
        bg.inputs["Color"].default_value = (0.18, 0.18, 0.18, 1.0)
    scene.render.film_transparent = False

def render_rgb(scene, rgb_path):
    """Render normal a PNG, sin compositor."""
    scene.render.use_compositing = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.filepath = rgb_path
    bpy.ops.render.render(write_still=True)

def render_depth(scene, cam, depth_path, depth_near, depth_far):
    """
    Segundo render con material override que mapea distancia de cámara a escala de grises.
    depth_near/depth_far = rango real de la escena para normalización correcta.
    """
    # Material que convierte View Distance → escala de grises normalizada
    mat = bpy.data.materials.new("__depth_override__")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    cam_node  = nt.nodes.new('ShaderNodeCameraData')
    map_range = nt.nodes.new('ShaderNodeMapRange')
    map_range.clamp = True

    # Usar índices de socket (robusto ante cambios de nombre en Blender 5.x)
    # inputs: 0=Value, 1=From Min, 2=From Max, 3=To Min, 4=To Max
    map_range.inputs[1].default_value = depth_near
    map_range.inputs[2].default_value = depth_far
    map_range.inputs[3].default_value = 1.0   # cercano = blanco
    map_range.inputs[4].default_value = 0.0   # lejano  = negro

    print(f"[DEPTH] near={depth_near:.2f}  far={depth_far:.2f}")

    emission = nt.nodes.new('ShaderNodeEmission')
    emission.inputs['Strength'].default_value = 1.0
    output   = nt.nodes.new('ShaderNodeOutputMaterial')

    # 'View Z Depth' = distancia perpendicular (depth buffer), mejor que 'View Distance'
    z_out = cam_node.outputs.get('View Z Depth') or cam_node.outputs.get('View Distance')
    nt.links.new(z_out,                            map_range.inputs[0])
    nt.links.new(map_range.outputs['Result'],       emission.inputs['Color'])
    nt.links.new(emission.outputs['Emission'],      output.inputs['Surface'])

    # Guardar materiales originales y aplicar override
    saved = {}
    for obj in scene.objects:
        if obj.type == 'MESH':
            saved[obj.name] = list(obj.data.materials)
            obj.data.materials.clear()
            obj.data.materials.append(mat)

    # Render depth (sin compositor, fondo negro)
    scene.render.use_compositing = False
    scene.render.film_transparent = True   # fondo negro = infinito
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'BW'
    scene.render.filepath = depth_path
    bpy.ops.render.render(write_still=True)

    # Restaurar materiales
    for obj in scene.objects:
        if obj.name in saved:
            obj.data.materials.clear()
            for m in saved[obj.name]:
                obj.data.materials.append(m)

    bpy.data.materials.remove(mat)

def main():
    args = parse_args()

    with open(args.dataset, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", {})
    dataset_dir = os.path.dirname(os.path.abspath(args.dataset))

    ids = sorted(items.keys()) if not args.ids else args.ids

    os.makedirs(args.out, exist_ok=True)

    for pid in ids:
        item = items.get(pid)
        if not item:
            print(f"[WARN] {pid} no encontrado en dataset")
            continue

        blend_path = item.get("blend_path")
        if not blend_path:
            print(f"[WARN] {pid} sin blend_path")
            continue

        abs_blend = abs_from_rel(args.dataset, blend_path)
        if not os.path.exists(abs_blend):
            print(f"[WARN] {pid} blend no existe: {abs_blend}")
            continue

        # Guardar junto al .blend en out_assets/pXXXX/
        out_dir    = os.path.dirname(abs_blend)
        rgb_path   = os.path.join(out_dir, f"{pid}_rgb.png")
        depth_path = os.path.join(out_dir, f"{pid}_depth.png")
        if args.skip_existing and os.path.exists(rgb_path) and os.path.exists(depth_path):
            print(f"[SKIP] {pid}")
            item["render_path"] = os.path.relpath(rgb_path,   dataset_dir).replace("\\", "/")
            item["depth_path"]  = os.path.relpath(depth_path, dataset_dir).replace("\\", "/")
            continue

        print(f"[START] {pid}")
        bpy.ops.wm.open_mainfile(filepath=abs_blend)

        scene = bpy.context.scene
        # Motor EEVEE (más rápido para pruebas)
        try:
            scene.render.engine = 'BLENDER_EEVEE_NEXT'
        except:
            scene.render.engine = 'BLENDER_EEVEE'

        if hasattr(scene, 'eevee') and hasattr(scene.eevee, 'taa_samples'):
            scene.eevee.taa_samples = 16

        scene.render.resolution_x = args.res[0]
        scene.render.resolution_y = args.res[1]
        scene.render.resolution_percentage = 100

        setup_world_bg(scene)
        cam, depth_near, depth_far = setup_camera_and_light(item, args.res[0], args.res[1])

        render_rgb(scene, rgb_path)
        render_depth(scene, cam, depth_path, depth_near, depth_far)

        # Guardar rutas relativas en el item
        item["render_path"] = os.path.relpath(rgb_path,   dataset_dir).replace("\\", "/")
        item["depth_path"]  = os.path.relpath(depth_path, dataset_dir).replace("\\", "/")
        print(f"[OK] {pid} -> {out_dir}/")

    # Guardar JSON actualizado
    from datetime import datetime, timezone
    data["meta"] = data.get("meta", {})
    data["meta"]["renders_depth_updated_at"] = datetime.now(timezone.utc).isoformat()
    data["meta"]["renders_depth_res"] = f"{args.res[0]}x{args.res[1]}"

    out_json = os.path.abspath(args.dataset)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[DONE] JSON actualizado: {out_json}")

if __name__ == "__main__":
    main()
