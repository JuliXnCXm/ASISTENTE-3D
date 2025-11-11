import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
largo = 10.0
ancho = 8.0
espesor = 0.3

# Crear la losa usando un cubo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -espesor / 2), # Centrada en el origen, debajo del plano XY
    scale=(largo, ancho, espesor)
)

losa = bpy.context.active_object
losa.name = "LosaCimentacion"