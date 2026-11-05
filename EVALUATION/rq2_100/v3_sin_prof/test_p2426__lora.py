import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho = 0.8
alto = 1.8
profundidad = 0.3
num_baldas = 4
espesor_panel = 0.02

# --- Creación de paneles laterales ---
ancho_util = ancho - espesor_panel * 2
pos_x_lateral = ancho / 2 - espesor_panel / 2
for i in range(2):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x_lateral if i == 0 else -pos_x_lateral, 0, alto / 2),
        scale=(espesor_panel, profundidad, alto)
    )
    bpy.context.active_object.name = f'Lateral_{i+1}'

# --- Creación de baldas ---
espacio_entre_baldas = alto / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_util, profundidad, espesor_panel)
    )
    bpy.context.active_object.name = f'Balda_{i+1}'