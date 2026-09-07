# generate_metric_depth.py
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
    name = ob.name.lower()
    pts = [ob.matrix_world @ Vector(p) for p in ob.bound_box]
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    sx = max(xs) - min(xs)
    sy = max(ys) - min(ys)
    sz = max(zs) - min(zs)
    max_xy = max(sx, sy, 0.001)
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

def get_sensor_size(sensor_fit, sensor_x, sensor_y):
    if sensor_fit == 'VERTICAL':
        return sensor_y
    return sensor_x

def get_camera_intrinsics(cam, res_x, res_y):
    focal_length = cam.data.lens
    sensor_x = cam.data.sensor_width
    sensor_y = cam.data.sensor_height
    sensor_fit = cam.data.sensor_fit

    pixel_aspect_ratio = bpy.context.scene.render.pixel_aspect_y / bpy.context.scene.render.pixel_aspect_x

    if sensor_fit == 'HORIZONTAL':
        view_fac_in_px = res_x
    else:
        view_fac_in_px = pixel_aspect_ratio * res_y * (sensor_x / sensor_y)

    pixel_size_mm_per_px = sensor_x / view_fac_in_px if view_fac_in_px > 0 else 0 # Prevent division by zero roughly
    
    # Calculate focal length in pixels
    fx = focal_length * res_x / get_sensor_size(sensor_fit, sensor_x, sensor_y)
    fy = focal_length * res_y * pixel_aspect_ratio / get_sensor_size(sensor_fit, sensor_x, sensor_y)
    
    cx = res_x / 2.0
    cy = res_y / 2.0
    
    return [[fx, 0, cx], [0, fy, cy], [0, 0, 1]]

def setup_camera_and_light(item, res_x, res_y):
    scene = bpy.context.scene

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

    light = scene.objects.get("RenderKeyLight")
    if light is None:
        light_data = bpy.data.lights.new("RenderKeyLight", type='AREA')
        light = bpy.data.objects.new("RenderKeyLight", light_data)
        scene.collection.objects.link(light)
    if light.data.type != 'AREA':
        light.data.type = 'AREA'

    col_name = item.get("asset_collection")
    objs = []
    if col_name and col_name in bpy.data.collections:
        objs = list(bpy.data.collections[col_name].objects)
    if not objs:
        objs = [o for o in scene.objects if o.type in {"MESH","CURVE","SURFACE","META","FONT"}]

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

    return cam

def setup_compositor_for_exr(scene, exr_path):
    """
    Configura el compositor para exportar la pasada Z (Profundidad) a un EXR de 32 bits.
    """
    bpy.context.window.scene = scene
    scene.use_nodes = True
    tree = scene.node_tree if hasattr(scene, 'node_tree') else None
    
    # En Blender 4.x/5.x a veces el node_tree no existe hasta que fuerzas la creación o usas un approach distinto
    if not tree:
        # Fallback: Solo renderizar y guardar la imagen si el compositor falla
        return False
        
    tree.nodes.clear()
    
    rl_node = tree.nodes.new(type="CompositorNodeRLayers")
    
    # Nodo de salida archivo
    file_out = tree.nodes.new(type="CompositorNodeOutputFile")
    file_out.base_path = os.path.dirname(exr_path)
    file_out.file_slots[0].path = os.path.basename(exr_path).replace(".exr", "_")
    file_out.format.file_format = 'OPEN_EXR'
    file_out.format.color_depth = '32'
    file_out.format.color_mode = 'RGB'  # Z pass is 1 channel, but EXR will save it
    
    tree.links.new(rl_node.outputs['Depth'], file_out.inputs[0])
    return True

def save_camera_meta(cam, res_x, res_y, json_path):
    K = get_camera_intrinsics(cam, res_x, res_y)
    
    # Matriz Extrínseca (World to Camera)
    world_to_cam = cam.matrix_world.inverted()
    
    meta = {
        "camera_type": "perspective",
        "resolution": [res_x, res_y],
        "intrinsics": K,
        "extrinsics_world_to_cam": [list(row) for row in world_to_cam],
        "cam_to_world": [list(row) for row in cam.matrix_world],
        "focal_length_mm": cam.data.lens,
        "clip_start": cam.data.clip_start,
        "clip_end": cam.data.clip_end
    }
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

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
            continue

        blend_path = item.get("blend_path")
        if not blend_path:
            continue

        abs_blend = abs_from_rel(args.dataset, blend_path)
        if not os.path.exists(abs_blend):
            continue

        out_dir    = os.path.dirname(abs_blend)
        exr_path   = os.path.join(out_dir, f"{pid}_depth.exr")
        cam_path   = os.path.join(out_dir, f"{pid}_camera.json")
        
        if args.skip_existing and os.path.exists(exr_path) and os.path.exists(cam_path):
            item["metric_depth_path"] = os.path.relpath(exr_path, dataset_dir).replace("\\", "/")
            item["camera_meta_path"]  = os.path.relpath(cam_path, dataset_dir).replace("\\", "/")
            continue

        print(f"[START] {pid} Metric Depth")
        bpy.ops.wm.open_mainfile(filepath=abs_blend)

        scene = bpy.context.scene
        
        # Necesitamos Cycles o Eevee configurado para sacar el pase Z (Depth) real
        scene.render.engine = 'BLENDER_EEVEE'
        scene.view_layers["ViewLayer"].use_pass_z = True
        
        scene.render.resolution_x = args.res[0]
        scene.render.resolution_y = args.res[1]
        scene.render.resolution_percentage = 100

        cam = setup_camera_and_light(item, args.res[0], args.res[1])
        
        # Guardamos EXR
        scene.render.filepath = exr_path
        scene.render.image_settings.file_format = 'OPEN_EXR'
        scene.render.image_settings.color_depth = '32'
        
        # Enable Z pass
        scene.view_layers["ViewLayer"].use_pass_z = True
        
        bpy.context.window.scene = scene
        scene.use_nodes = True
        tree = scene.node_tree if hasattr(scene, 'node_tree') else None
        
        if tree:
            tree.nodes.clear()
            rl_node = tree.nodes.new(type="CompositorNodeRLayers")
            file_out = tree.nodes.new(type="CompositorNodeOutputFile")
            file_out.base_path = os.path.dirname(exr_path)
            # We save directly to avoid frame numbers getting appended if possible
            file_out.file_slots[0].path = os.path.basename(exr_path).replace(".exr", "_")
            file_out.format.file_format = 'OPEN_EXR'
            file_out.format.color_depth = '32'
            tree.links.new(rl_node.outputs['Depth'], file_out.inputs[0])

        save_camera_meta(cam, args.res[0], args.res[1], cam_path)

        # Render - write still is false, but we need to set filepath to avoid /tmp errors
        scene.render.filepath = os.path.join(out_dir, f"{pid}_dummy")
        bpy.ops.render.render(write_still=True)

        # Buscar el EXR generado (el File Output node siempre anexa números, ej: p0001_depth__0001.exr)
        # y renombrarlo
        base_name = os.path.basename(exr_path).replace(".exr", "_")
        
        # Intenta varias combinaciones comunes de Blender
        possible_names = [
            f"{base_name}0000.exr",
            f"{base_name}0001.exr",
            f"{base_name}.exr",
            f"{base_name}_0001.exr",
            f"{pid}_dummy.exr",
            f"{pid}_dummy0000.exr",
            f"{pid}_dummy0001.exr"
        ]
        
        found = False
        for p_name in possible_names:
            full_p = os.path.join(out_dir, p_name)
            if os.path.exists(full_p):
                if os.path.exists(exr_path):
                    os.remove(exr_path)
                os.rename(full_p, exr_path)
                found = True
                break
                
        if not found:
            # Fallback de búsqueda con glob
            import glob
            matches = glob.glob(os.path.join(out_dir, f"*{base_name}*.exr"))
            if matches:
                if os.path.exists(exr_path):
                    os.remove(exr_path)
                os.rename(matches[0], exr_path)
                found = True
                
        if not found:
            print(f"[WARN] No se encontró el EXR exportado para {pid}")

        item["metric_depth_path"] = os.path.relpath(exr_path, dataset_dir).replace("\\", "/")
        item["camera_meta_path"]  = os.path.relpath(cam_path, dataset_dir).replace("\\", "/")
        print(f"[OK] {pid} -> EXR y Camera Meta.")

    # Guardar JSON actualizado
    data["meta"]["depth_status"] = "metric_exr_and_camera_metadata_included"
    
    out_json = os.path.abspath(args.dataset)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
