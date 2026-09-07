import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

altura = 0.9
diametro = 0.3
radio = diametro / 2

bpy.ops.mesh.primitive_cylinder_add(
    radius=radio,
    depth=altura,
    location=(0, 0, altura / 2),
    vertices=32
)

bolardo = bpy.context.active_object
bolardo.name = 'Bolardo_Hormigon'

bpy.ops.object.shade_smooth()