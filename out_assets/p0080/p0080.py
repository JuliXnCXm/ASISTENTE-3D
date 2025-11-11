import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
ancho = 5.0
profundidad = 5.0
espesor = 0.20

# Crear la losa usando un cubo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, -espesor / 2) # Centrada en el origen, sobre el plano XY
)

# Escalar el cubo a las dimensiones deseadas
losa = bpy.context.active_object
losa.name = 'LosaDePiso'
losa.scale = (ancho / 2, profundidad / 2, espesor / 2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)