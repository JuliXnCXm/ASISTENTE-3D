#!/usr/bin/env python3
"""
build_edit_artifacts.py
Ejecuta el código `after_python_code` del dataset de edición en Blender
para generar los archivos `.blend` y `.png` (RGB) para validación manual.
"""

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
    ap.add_argument("--dsl-dir", required=True)
    ap.add_argument("--ids", nargs="*", default=None)
    ap.add_argument("--skip-existing", action="store_true")
    return ap.parse_args(argv)

def clean_scene():
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def run_script(code_str, dsl_dir):
    if dsl_dir not in sys.path:
        sys.path.insert(0, dsl_dir)
    g = {"__name__": "__main__"}
    try:
        import os, math, random, json
        import mathutils
        g["os"] = os
        g["sys"] = sys
        g["math"] = math
        g["random"] = random
        g["json"] = json
        g["mathutils"] = mathutils
        import blender_arch as A
        g["A"] = A
    except Exception:
        pass
    exec(compile(code_str, "<string>", "exec"), g, g)

def setup_camera_and_light():
    scene = bpy.context.scene
    
    # Asegurarnos de que el world tiene un color base, de lo contrario todo será oscuro
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    bg_node = scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = (0.5, 0.5, 0.5, 1)

    cam = scene.objects.get("RenderCam") or bpy.data.objects.new("RenderCam", bpy.data.cameras.new("RenderCam"))
    if cam.name not in scene.collection.objects:
        scene.collection.objects.link(cam)
    scene.camera = cam

    cam.data.lens = 35.0
    cam.data.sensor_width = 36.0
    cam.data.sensor_height = 24.0

    light = scene.objects.get("RenderKeyLight") or bpy.data.objects.new("RenderKeyLight", bpy.data.lights.new("RenderKeyLight", type='AREA'))
    if light.name not in scene.collection.objects:
        scene.collection.objects.link(light)

    objs = [o for o in scene.objects if o.type == 'MESH']
    
    # Bounding Box Simple
    mins = Vector(( float('inf'),  float('inf'),  float('inf')))
    maxs = Vector((-float('inf'), -float('inf'), -float('inf')))
    any_ok = False
    for ob in objs:
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
        mins, maxs = Vector((-1,-1,0)), Vector((1,1,2))

    center = (mins + maxs) * 0.5
    size   = (maxs - mins)
    max_dim = max(size.x, size.y, size.z, 0.001)

    fov_v = 2.0 * math.atan((cam.data.sensor_height / 2.0) / cam.data.lens)
    half_diag = math.sqrt(size.x**2 + size.y**2 + size.z**2) * 0.5
    dist = (half_diag / math.tan(fov_v * 0.5)) * 1.5

    az = math.radians(45.0)
    el = math.radians(35.0)
    cam.location = Vector((
        center.x + dist * math.cos(el) * math.sin(az),
        center.y - dist * math.cos(el) * math.cos(az),
        center.z + dist * math.sin(el),
    ))
    
    # Look at
    forward = (center - cam.location).normalized()
    right = forward.cross(Vector((0,0,1))).normalized()
    up2 = right.cross(forward).normalized()
    cam.rotation_euler = Matrix(((right.x, up2.x, -forward.x), (right.y, up2.y, -forward.y), (right.z, up2.z, -forward.z))).to_euler()

    light.location = Vector((center.x - max_dim * 0.5, center.y - max_dim * 0.5, center.z + max_dim * 2.0))
    light.rotation_euler = (math.radians(-45), 0.0, math.radians(-30))
    light.data.energy = max(2000.0, max_dim * 500) # Energía aumentada masivamente
    light.data.size = max(max_dim, 10.0) # Tamaño aumentado para iluminar toda la escena
    
    # Añadir luz de relleno
    fill_light = scene.objects.get("RenderFillLight") or bpy.data.objects.new("RenderFillLight", bpy.data.lights.new("RenderFillLight", type='AREA'))
    if fill_light.name not in scene.collection.objects:
        scene.collection.objects.link(fill_light)
        
    fill_light.location = Vector((center.x + max_dim, center.y + max_dim, center.z + max_dim))
    fill_light.rotation_euler = (math.radians(45), 0.0, math.radians(135))
    fill_light.data.energy = light.data.energy * 0.5
    fill_light.data.size = light.data.size

def main():
    args = parse_args()

    with open(args.dataset, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", {})

    ids = sorted(items.keys()) if not args.ids else args.ids
    os.makedirs(args.out, exist_ok=True)
    dataset_dir = os.path.dirname(os.path.abspath(args.dataset))

    for pid in ids:
        item = items.get(pid)
        if not item:
            continue

        out_dir = os.path.join(args.out, pid)
        os.makedirs(out_dir, exist_ok=True)
        
        blend_path = os.path.join(out_dir, f"{pid}_after.blend")
        rgb_path = os.path.join(out_dir, f"{pid}_after_rgb.png")
        
        if args.skip_existing and os.path.exists(blend_path) and os.path.exists(rgb_path):
            item["after_blend_path"] = os.path.relpath(blend_path, dataset_dir).replace("\\", "/")
            item["after_render_path"] = os.path.relpath(rgb_path, dataset_dir).replace("\\", "/")
            continue

        print(f"[START] {pid} Edit Artifacts")
        
        try:
            clean_scene()
            code = item["after_python_code"]
            run_script(code, args.dsl_dir)
            
            # Guardar .blend
            bpy.ops.wm.save_as_mainfile(filepath=blend_path, compress=True)
            
            # Guardar RGB
            scene = bpy.context.scene
            try:
                scene.render.engine = 'BLENDER_EEVEE_NEXT'
            except:
                scene.render.engine = 'BLENDER_EEVEE'
                
            scene.render.resolution_x = 512
            scene.render.resolution_y = 512
            setup_camera_and_light()
            
            scene.render.filepath = rgb_path
            scene.render.image_settings.file_format = 'PNG'
            scene.render.use_compositing = False
            bpy.ops.render.render(write_still=True)
            
            item["after_blend_path"] = os.path.relpath(blend_path, dataset_dir).replace("\\", "/")
            item["after_render_path"] = os.path.relpath(rgb_path, dataset_dir).replace("\\", "/")
            print(f"[OK] {pid}")
            
        except Exception as e:
            print(f"[ERROR] {pid}: {e}")

    # Guardar JSON actualizado
    out_json = os.path.abspath(args.dataset)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
