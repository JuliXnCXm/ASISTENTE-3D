import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo_muro = 10.0
altura_muro = 2.0
espesor_muro = 0.2

bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, altura_muro / 2),
    scale=(espesor_muro / 2, largo_muro / 2, altura_muro / 2)
)

muro = bpy.context.active_object
muro.name = 'MuroCerramiento'