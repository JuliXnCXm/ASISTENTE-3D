import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Dimensiones de la losa
ancho_x = 6.0
profundidad_y = 8.0
espesor_z = 0.20

# Crear la losa
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho_x / 2, profundidad_y / 2, -espesor_z / 2)
)
losa = bpy.context.active_object
losa.name = "LosaPiso"

# Aplicar dimensiones
losa.dimensions = (ancho_x, profundidad_y, espesor_z)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)