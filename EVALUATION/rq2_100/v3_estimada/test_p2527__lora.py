import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho = 1.2
alto = 2.0
profundidad = 0.3
num_baldas = 5
grosor_panel = 0.02

# --- Creación de los paneles laterales ---
ancho_util = ancho - grosor_panel * 2
pos_x_lateral = ancho / 2 - grosor_panel / 2
for i in range(2):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x_lateral if i == 0 else -pos_x_lateral, 0, alto / 2),
        scale=(grosor_panel, profundidad, alto)
    )
    bpy.context.object.name = f'Lateral_{i}'

# --- Creación de las baldas ---
espacio_entre_baldas = alto / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_util, profundidad, grosor_panel)
    )
    bpy.context.object.name = f'Balda_{i}'