import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
ancho_x = 6.0
profundidad_y = 4.0
espesor_z = 0.20

# Crear la losa usando un cubo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -espesor_z / 2.0), # Se ubica para que la cara superior quede en Z=0
    scale=(ancho_x, profundidad_y, espesor_z)
)

losa = bpy.context.active_object
losa.name = 'LosaPiso'