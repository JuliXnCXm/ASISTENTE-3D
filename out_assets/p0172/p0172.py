import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho = 12.0
profundidad = 12.0
espesor = 0.4

# Crear la losa
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(0, 0, -espesor / 2), # Centrada en XY, con la cara superior en Z=0
    scale=(ancho, profundidad, espesor)
)

losa = bpy.context.active_object
losa.name = "LosaCimentacion"

# Aplicar la escala para que las dimensiones sean exactas
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)