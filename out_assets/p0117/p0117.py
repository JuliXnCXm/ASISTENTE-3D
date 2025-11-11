import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la losa ---
ancho = 6.0
profundidad = 6.0
espesor = 0.25

# --- Creación de la losa ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, -espesor / 2),
    scale=(ancho, profundidad, espesor)
)
losa = bpy.context.active_object
losa.name = "LosaPiso"