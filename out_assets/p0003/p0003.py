import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo_x = 4.0
largo_y = 3.0
altura = 2.7
espesor = 0.2

# Muro en eje X
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_x / 2, espesor / 2, altura / 2),
    scale=(largo_x, espesor, altura)
)

# Muro en eje Y
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(espesor / 2, largo_y / 2, altura / 2),
    scale=(espesor, largo_y, altura)
)