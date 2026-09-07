import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

altura_bolardo = 0.8
radio_bolardo = 0.1 # Diámetro 0.2

bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,
    radius=radio_bolardo,
    depth=altura_bolardo,
    location=(0, 0, altura_bolardo / 2)
)

bolardo = bpy.context.active_object
bolardo.name = 'Bolardo_Hormigon'
bpy.ops.object.shade_smooth()