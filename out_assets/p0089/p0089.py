import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
ancho_x = 4.0
largo_y = 5.0
espesor_z = 0.2

# Crear la losa usando un cubo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, -espesor_z / 2),
    scale=(ancho_x, largo_y, espesor_z)
)

# Renombrar el objeto
losa = bpy.context.active_object
losa.name = 'LosaPiso'