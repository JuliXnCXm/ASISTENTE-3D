import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

altura_muro = 2.5
espesor_muro = 0.15
largo_muro_x = 4.0
largo_muro_y = 3.0

# Muro a lo largo del eje X
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_muro_x / 2, espesor_muro / 2, altura_muro / 2),
    scale=(largo_muro_x, espesor_muro, altura_muro)
)
muro_x = bpy.context.active_object
muro_x.name = 'Muro_Eje_X'

# Muro a lo largo del eje Y
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(espesor_muro / 2, largo_muro_y / 2, altura_muro / 2),
    scale=(espesor_muro, largo_muro_y, altura_muro)
)
muro_y = bpy.context.active_object
muro_y.name = 'Muro_Eje_Y'