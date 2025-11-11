import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
alto = 3.0
espesor = 0.25
largo_x = 6.0
largo_y = 4.0

# Crear muro en eje X
loc_x = (largo_x - espesor) / 2
loc_z = alto / 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(loc_x, 0, loc_z)
)
muro_x = bpy.context.active_object
muro_x.name = 'MuroX'
muro_x.dimensions = (largo_x - espesor, espesor, alto)

# Crear muro en eje Y
loc_y = (largo_y - espesor) / 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-espesor/2, loc_y, loc_z)
)
muro_y = bpy.context.active_object
muro_y.name = 'MuroY'
muro_y.dimensions = (espesor, largo_y, alto)

# Unir muros en un solo objeto para una esquina limpia
bpy.ops.object.select_all(action='DESELECT')
muro_x.select_set(True)
muro_y.select_set(True)
bpy.context.view_layer.objects.active = muro_x
bpy.ops.object.join()