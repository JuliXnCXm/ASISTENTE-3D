# render_blends_from_dataset.py
# Recorre un dataset con items.{id}.blend_path y genera un PNG por .blend
# Además, añade items.{id}.render_path al JSON de salida.
#
# Uso:
# blender -b -P render_blends_from_dataset.py -- --dataset dataset_with_blends.json --out renders
# Opciones:
#   --ids p0001 p0002 ...       (opcional: subset)
#   --engine cycles|eevee       (por defecto: cycles)
#   --res 1600 1200             (ancho alto, por defecto: 1600 1200)
#   --samples 64                (muestras Cycles/EEVEE, por defecto 64)
#   --transparent               (fondo transparente)
#   --bg 0.95 0.95 0.98         (color de fondo si no es transparente)
#   --skip-existing             (no vuelve a renderizar si el PNG existe)
#   --update-json-out out.json  (opcional; por defecto: <dataset> con _with_renders.json)

import bpy
import os
import sys
import json
import math
import argparse
from mathutils import Vector, Matrix
from datetime import datetime, timezone

def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, help="Ruta al JSON que contiene items.{id}.blend_path")
    ap.add_argument("--out", required=True, help="Carpeta raíz donde escribir los PNG")
    ap.add_argument("--update-json-out", default=None, help="Ruta JSON actualizado (si se omite, <dataset>_with_renders.json)")
    ap.add_argument("--ids", nargs="*", help="IDs específicos a renderizar")
    ap.add_argument("--engine", choices=["cycles", "eevee"], default="cycles")
    ap.add_argument("--res", nargs=2, type=int, default=[1600, 1200], help="Resolución: ancho alto")
    ap.add_argument("--samples", type=int, default=64, help="Muestras de render")
    ap.add_argument("--transparent", action="store_true", help="Fondo transparente")
    ap.add_argument("--bg", nargs=3, type=float, default=[0.18, 0.18, 0.18], help="Color de fondo RGB [0-1]")
    ap.add_argument("--skip-existing", action="store_true", help="No renderizar si el PNG ya existe")
    return ap.parse_args(argv)

def abs_from_rel(base_json_path, maybe_rel_path):
    if os.path.isabs(maybe_rel_path):
        return maybe_rel_path
    base_dir = os.path.dirname(os.path.abspath(base_json_path))
    return os.path.abspath(os.path.join(base_dir, maybe_rel_path))

def set_engine(engine:str, samples:int, transparent:bool, bg_color):
    scene = bpy.context.scene
    if engine == "cycles":
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = samples
        # Denoising simple
        if hasattr(scene.cycles, "use_denoising"):
            scene.cycles.use_denoising = True
    else:
        # EEVEE (funciona tanto 'BLENDER_EEVEE' como 'BLENDER_EEVEE_NEXT' según versión)
        try:
            scene.render.engine = 'BLENDER_EEVEE'
        except:
            scene.render.engine = 'BLENDER_EEVEE_NEXT'
        if hasattr(scene.eevee, "taa_samples"):
            scene.eevee.taa_samples = samples

    # Fondo
    if transparent:
        scene.render.film_transparent = True
    else:
        scene.render.film_transparent = False
        # Color fondo world
        world = scene.world or bpy.data.worlds.new("World")
        scene.world = world
        if world.use_nodes:
            nt = world.node_tree
            bg = nt.nodes.get("Background") or nt.nodes.new("ShaderNodeBackground")
            bg.inputs["Color"].default_value = (bg_color[0], bg_color[1], bg_color[2], 1.0)

def set_resolution(width:int, height:int):
    r = bpy.context.scene.render
    r.resolution_x = width
    r.resolution_y = height
    r.resolution_percentage = 100

def look_at(cam_obj, target:Vector, up=Vector((0,0,1))):
    """Alinea la cámara para mirar al 'target'. La cámara en Blender mira por -Z local y Y es 'arriba' local."""
    loc = cam_obj.location
    forward = (target - loc).normalized()
    right = forward.cross(up).normalized()
    up2 = right.cross(forward).normalized()
    # Matriz con ejes: X=right, Y=up2, Z=-forward
    rot = Matrix((
        (right.x,  up2.x, -forward.x),
        (right.y,  up2.y, -forward.y),
        (right.z,  up2.z, -forward.z),
    ))
    cam_obj.rotation_euler = rot.to_euler()

def compute_bbox_world(objs):
    """Devuelve (min_v, max_v) del AABB mundial de una lista de objetos (sólo los con .type en {'MESH','CURVE','SURFACE','META'})"""
    types_ok = {"MESH","CURVE","SURFACE","META","FONT"}
    mins = Vector(( float('inf'),  float('inf'),  float('inf')))
    maxs = Vector((-float('inf'), -float('inf'), -float('inf')))
    any_ok = False
    for ob in objs:
        if ob.type not in types_ok:
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
        # fallback al origen con tamaño unitario mínimo
        return Vector((-0.5,-0.5,0.0)), Vector((0.5,0.5,1.0))
    return mins, maxs

def ensure_camera_and_light():
    scene = bpy.context.scene
    cam = next((ob for ob in scene.objects if ob.type == 'CAMERA'), None)
    if cam is None:
        cam_data = bpy.data.cameras.new("RenderCam")
        cam = bpy.data.objects.new("RenderCam", cam_data)
        scene.collection.objects.link(cam)
    # Luz — siempre usamos una AREA light propia para poder setear size
    light = scene.objects.get("RenderKeyLight")
    if light is None:
        light_data = bpy.data.lights.new("RenderKeyLight", type='AREA')
        light = bpy.data.objects.new("RenderKeyLight", light_data)
        scene.collection.objects.link(light)
    # Forzar tipo AREA (por si el datablock fue reutilizado)
    if light.data.type != 'AREA':
        light.data.type = 'AREA'
    light.data.energy = 2000.0
    light.data.shape = 'RECTANGLE'
    scene.camera = cam
    return cam, light

def frame_asset(cam, light, objs, res_x, res_y, margin=0.25):
    """Vista isométrica 3/4 elevada: ángulo horizontal 45°, elevación 35°."""
    scene = bpy.context.scene
    mins, maxs = compute_bbox_world(objs)
    center = (mins + maxs) * 0.5
    size   = (maxs - mins)
    max_dim = max(size.x, size.y, size.z, 0.001)

    cam_data = cam.data
    cam_data.lens        = 35.0    # gran angular suave — captura más escena
    cam_data.sensor_width  = 36.0
    cam_data.sensor_height = 24.0
    cam_data.clip_start  = 0.01
    cam_data.clip_end    = 10000.0

    # FOV diagonal — usamos el menor (vertical) para garantizar encuadre
    fov_v = 2.0 * math.atan((cam_data.sensor_height / 2.0) / cam_data.lens)

    # Distancia base para que el objeto quepa en frame vertical
    half_diag = math.sqrt(size.x**2 + size.y**2 + size.z**2) * 0.5
    dist = (half_diag / math.tan(fov_v * 0.5)) * (1.0 + margin)

    # Vista 3/4: 45° horizontal, 35° de elevación
    az = math.radians(45.0)   # azimut
    el = math.radians(35.0)   # elevación

    cam.location = Vector((
        center.x + dist * math.cos(el) * math.sin(az),
        center.y - dist * math.cos(el) * math.cos(az),
        center.z + dist * math.sin(el),
    ))
    look_at(cam, center)

    # Luz principal desde arriba-frente, opuesta al eje de cámara
    light.location = Vector((
        center.x - max_dim * 0.5,
        center.y - max_dim * 0.5,
        center.z + max_dim * 2.0,
    ))
    light.rotation_euler = (math.radians(-45), 0.0, math.radians(-30))
    light.data.energy = 800.0
    light.data.size   = max(max_dim * 0.8, 0.5)
    if hasattr(light.data, "size_y"):
        light.data.size_y = max(max_dim * 0.8, 0.5)

def get_asset_objects_from_item(item):
    """Intenta recuperar los objetos de la colección creada por build_blends_from_dataset."""
    col_name = item.get("asset_collection")
    objs = []
    if col_name and col_name in bpy.data.collections:
        col = bpy.data.collections[col_name]
        objs = list(col.objects)
    else:
        # fallback: todos los MESH visibles
        objs = [o for o in bpy.context.scene.objects if o.type in {"MESH","CURVE","SURFACE","META","FONT"}]
    return objs

# Categorías de espacios interiores donde ocultar paredes revela el contenido
ENCLOSED_CATEGORIES = {"habitacion", "apartamento", "oficina",
                        "cocina", "baño", "salon", "comedor", "dormitorio"}

# Keywords en el nombre del objeto que indican muro/techo a ocultar
WALL_NAME_KEYWORDS = ("muro", "pared", "wall", "tabique", "cerramiento", "techo", "cubierta")

def isolate_collection(item):
    """Oculta todo excepto la colección del asset si existe."""
    col_name = item.get("asset_collection")
    if not col_name:
        return
    scene = bpy.context.scene
    for c in scene.collection.children:
        c.hide_render = (c.name != col_name)
        c.hide_viewport = (c.name != col_name)

def hide_walls_if_enclosed(item):
    """Solo para espacios interiores cerrados: oculta muros y techos para ver el contenido."""
    category = item.get("category", "").lower().strip()
    domain   = item.get("domain",   "").lower().strip()
    # Solo aplica a items con dominio interior Y categoría de espacio cerrado
    if domain != "interior" or category not in ENCLOSED_CATEGORIES:
        return
    hidden = []
    for obj in bpy.context.scene.objects:
        name_lower = obj.name.lower()
        if any(kw in name_lower for kw in WALL_NAME_KEYWORDS):
            obj.hide_render   = True
            obj.hide_viewport = True
            hidden.append(obj.name)
    if hidden:
        print(f"[INFO] {len(hidden)} objetos ocultos para render interior")

def main():
    args = parse_args()

    with open(args.dataset, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", {})
    if not isinstance(items, dict) or not items:
        raise SystemExit("El JSON no contiene 'items' válidos.")

    if args.update_json_out:
        out_json = args.update_json_out
    else:
        base = os.path.splitext(os.path.basename(args.dataset))[0]
        out_json = os.path.join(os.path.dirname(args.dataset), f"{base}_with_renders.json")

    # Subset de IDs
    ids = sorted(items.keys()) if not args.ids else [i for i in args.ids if i in items]

    os.makedirs(args.out, exist_ok=True)

    for pid in ids:
        item = items[pid]
        blend_path = item.get("blend_path")
        if not blend_path:
            print(f"[WARN] {pid} no tiene 'blend_path', se omite.")
            continue

        abs_blend = abs_from_rel(args.dataset, blend_path)
        if not os.path.exists(abs_blend):
            print(f"[WARN] {pid} blend no encontrado: {abs_blend}")
            continue

        # Ruta de salida PNG
        out_dir = os.path.join(args.out, pid)
        os.makedirs(out_dir, exist_ok=True)
        png_path = os.path.join(out_dir, f"{pid}.png")
        if args.skip_existing and os.path.exists(png_path):
            # Actualiza render_path si no estaba
            rel_png = os.path.relpath(png_path, start=os.path.dirname(out_json)).replace("\\","/")
            item["render_path"] = rel_png
            print(f"[SKIP] {pid} (ya existe)")
            continue

        # Abrir el .blend
        bpy.ops.wm.open_mainfile(filepath=abs_blend)

        # Ajustar motor, resolución y fondo
        set_engine(args.engine, args.samples, args.transparent, args.bg)
        set_resolution(args.res[0], args.res[1])

        # Aislar colección del asset si existe
        isolate_collection(item)

        # Ocultar paredes en espacios cerrados para ver interior
        hide_walls_if_enclosed(item)

        # Cámara + luz
        cam, light = ensure_camera_and_light()

        # Encadre
        objs = get_asset_objects_from_item(item)
        frame_asset(cam, light, objs, args.res[0], args.res[1], margin=0.25)

        # Render
        scene = bpy.context.scene
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = png_path
        bpy.ops.render.render(write_still=True)

        # Guardar ruta relativa en JSON
        rel_png = os.path.relpath(png_path, start=os.path.dirname(out_json)).replace("\\","/")
        item["render_path"] = rel_png
        print(f"[OK] {pid} -> {png_path}")

    # Meta y guardado de JSON
    data["meta"] = data.get("meta", {})
    data["meta"]["renders_output_root"] = os.path.abspath(args.out).replace("\\","/")
    data["meta"]["renders_updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[DONE] Render finalizado. JSON actualizado: {out_json}")

if __name__ == "__main__":
    main()
