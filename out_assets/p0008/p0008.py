import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

diametro = 3.0
espesor = 0.02

bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro / 2,
    depth=espesor,
    location=(0, 0, espesor / 2),
    vertices=128
)