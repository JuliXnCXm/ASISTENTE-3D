import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

altura_bolardo = 0.80
diametro_bolardo = 0.20
separacion = 1.5
num_bolardos = 3

for i in range(num_bolardos):
    loc_y = (i - (num_bolardos - 1) / 2) * separacion
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diametro_bolardo / 2,
        depth=altura_bolardo,
        location=(0, loc_y, altura_bolardo / 2)
    )
    bolardo = bpy.context.active_object
    bolardo.name = f"Bolardo.{i+1:03d}"