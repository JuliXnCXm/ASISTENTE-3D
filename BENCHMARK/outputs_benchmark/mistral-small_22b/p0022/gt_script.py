import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 5.0
alto = 2.8
espesor = 0.15

bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(largo / 2, 0, alto / 2),
    scale=(largo, espesor, alto)
)

muro = bpy.context.active_object
muro.name = 'MuroDivisorio'