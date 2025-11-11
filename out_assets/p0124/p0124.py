import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la alfombra ---
diametro = 3.0
espesor = 0.015

# --- Creación de la alfombra ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro / 2,
    depth=espesor,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, espesor / 2),
    vertices=64 # Para un borde más suave
)
alfombra = bpy.context.active_object
alfombra.name = "AlfombraCircular"