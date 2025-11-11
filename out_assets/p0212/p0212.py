import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración de la escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Dimensiones de la losa
largo = 10.0
ancho = 8.0
espesor = 0.4

# --- Creación de la losa
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, -espesor / 2) # Se apoya sobre el plano XY
)
losa = bpy.context.active_object
losa.name = 'LosaCimentacion'

# --- Aplicar dimensiones
losa.dimensions = (largo, ancho, espesor)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)