import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_muro1 = 4.0
largo_muro2 = 3.0
altura = 2.5
espesor = 0.15

# Muro 1 (en eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_muro1 / 2, espesor / 2, altura / 2),
    scale=(largo_muro1, espesor, altura)
)
bpy.context.object.name = "Muro_X"

# Muro 2 (en eje Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-espesor / 2, largo_muro2 / 2, altura / 2),
    scale=(espesor, largo_muro2, altura)
)
bpy.context.object.name = "Muro_Y"