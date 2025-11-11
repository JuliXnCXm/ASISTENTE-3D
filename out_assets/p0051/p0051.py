import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
largo_x = 5.0
ancho_y = 4.0
espesor_z = 0.20

# Crear la losa de piso
# La ubicación en Z se ajusta para que la cara superior quede en Z=0
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_x / 2, ancho_y / 2, -espesor_z / 2),
    scale=(largo_x, ancho_y, espesor_z)
)

# Renombrar el objeto
bpy.context.active_object.name = 'LosaPiso'