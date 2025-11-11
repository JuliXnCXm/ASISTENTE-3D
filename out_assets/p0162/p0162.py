import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

dimension_losa = 4.0
espesor_losa = 0.15

bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, -espesor_losa / 2),
    scale=(dimension_losa, dimension_losa, espesor_losa)
)

losa_patio = bpy.context.active_object
losa_patio.name = 'LosaPatio'