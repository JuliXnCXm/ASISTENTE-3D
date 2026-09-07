import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 6.0
ancho = 4.0
espesor = 0.20

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo / 2, ancho / 2, -espesor / 2),
    scale=(largo, ancho, espesor)
)
losa = bpy.context.active_object
losa.name = "LosaDePiso"