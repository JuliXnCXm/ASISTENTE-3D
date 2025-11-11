import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

ancho = 5.0
largo = 7.0
espesor = 0.25

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho / 2, largo / 2, -espesor / 2),
    scale=(ancho, largo, espesor)
)

losa = bpy.context.active_object
losa.name = "LosaPatio"