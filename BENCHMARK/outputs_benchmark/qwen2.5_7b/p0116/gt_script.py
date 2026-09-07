import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del muro ---
longitud = 5.0
altura = 2.7
espesor = 0.15

# --- Creación del muro ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(longitud / 2, 0, altura / 2),
    scale=(longitud, espesor, altura)
)
muro = bpy.context.active_object
muro.name = "MuroSimple"