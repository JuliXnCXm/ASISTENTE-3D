import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de los bolardos ---
cantidad = 3
alto = 0.9
diametro = 0.2
separacion = 1.5
radio = diametro / 2

# --- Bucle para crear los bolardos ---
for i in range(cantidad):
    pos_x = i * separacion
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radio,
        depth=alto,
        location=(pos_x, 0, alto / 2)
    )
    bolardo = bpy.context.active_object
    bolardo.name = f"Bolardo.{i+1:03d}"