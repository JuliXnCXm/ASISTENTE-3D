import bpy

bpy.ops.wm.read_homefile(use_empty=True)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

dimension_x = 4.0
dimension_y = 4.0
espesor = 0.2

bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, -espesor / 2),
    scale=(dimension_x, dimension_y, espesor)
)

losa = bpy.context.active_object
losa.name = 'LosaHormigon'