import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

altura_bolardo = 0.9
radio_bolardo = 0.15 # Diámetro de 0.3 m

bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_bolardo,
    depth=altura_bolardo,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, altura_bolardo / 2),
    scale=(1, 1, 1)
)

bolardo = bpy.context.active_object
bolardo.name = 'Bolardo'