import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo_norte = 5.0
largo_oeste = 4.0
altura = 2.7
espesor = 0.15

# Muro Norte
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_norte / 2, -espesor / 2, altura / 2),
    scale=(largo_norte, espesor, altura)
)
bpy.context.active_object.name = 'MuroNorte'

# Muro Oeste
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-espesor / 2, largo_oeste / 2 - espesor, altura / 2),
    scale=(espesor, largo_oeste, altura)
)
bpy.context.active_object.name = 'MuroOeste'