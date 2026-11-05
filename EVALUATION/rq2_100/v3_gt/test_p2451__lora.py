import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 1.8
fondo = 0.3
num_baldas = 5

# Paneles laterales
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * (ancho / 2), 0, alto / 2),
        scale=(fondo, fondo, alto)
    )
    bpy.context.active_object.name = f'Lateral_{i}'

# Baldas
espacio_entre_baldas = alto / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho, fondo, 0.02)
    )
    bpy.context.active_object.name = f'Balda_{i}'