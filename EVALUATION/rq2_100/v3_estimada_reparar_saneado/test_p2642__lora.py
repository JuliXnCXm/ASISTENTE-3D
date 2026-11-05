import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 0.8
profundidad = 0.3
alto_total = 1.8
num_baldas = 5

# Paneles laterales
ancho_util = ancho - 2 * profundidad
pos_x_lateral = profundidad / 2
for i in range(2):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x_lateral if i == 0 else -pos_x_lateral, 0, alto_total / 2),
        scale=(profundidad, ancho_util, alto_total)
    )
    bpy.context.active_object.name = f'Lateral_{i+1}'

# Baldas
espacio_entre_baldas = alto_total / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_util, profundidad, 0.04)
    )
    bpy.context.active_object.name = f'Balda_{i+1}'