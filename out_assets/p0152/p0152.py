import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
ancho = 8.0
largo = 8.0
espesor = 0.3

# Crear la losa
# La ubicación se establece en z = -espesor/2 para que la cara superior quede en z=0
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -espesor / 2),
    scale=(largo, ancho, espesor)
)
losa = bpy.context.active_object
losa.name = "LosaCimentacion"