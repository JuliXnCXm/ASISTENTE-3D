import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

num_peldanos = 12
huella = 0.28
contrahuella = 0.18
ancho = 1.0

for i in range(num_peldanos):
    loc_x = i * huella + huella / 2
    loc_y = 0
    loc_z = i * contrahuella + contrahuella / 2

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(loc_x, loc_y, loc_z),
        scale=(huella, ancho, contrahuella)
    )
    peldano = bpy.context.active_object
    peldano.name = f'Peldano_{i+1:02d}'