import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 0.8
alto = 1.8
profundidad = 0.3
grosor_madera = 0.02

# Paneles laterales
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * (ancho / 2) + grosor_madera / 2, 0, alto / 2),
        scale=(grosor_madera, profundidad, alto)
    )
    bpy.context.object.name = f'Lateral_{i}'

# Baldas
num_baldas = 4
espacio_entre_baldas = alto / (num_baldas - 1)

for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho - 2 * grosor_madera, profundidad, grosor_madera)
    )
    bpy.context.object.name = f'Balda_{i}'