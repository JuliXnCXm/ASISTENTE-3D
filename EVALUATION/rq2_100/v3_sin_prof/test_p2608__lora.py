import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 1.2
ancho_total = 0.8
fondo_total = 0.3
grosor_panel = 0.02
num_baldas = 3

# --- Creación de paneles laterales ---
ancho_balda = ancho_total / 2
pos_x_lateral = ancho_balda + grosor_panel / 2

for i in range(2):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x_lateral if i == 0 else -pos_x_lateral, 0, alto_total / 2),
        scale=(grosor_panel, fondo_total, alto_total)
    )
    bpy.context.active_object.name = f'Lateral_{i+1}'

# --- Creación de baldas ---
espacio_entre_baldas = alto_total / (num_baldas + 1)

for i in range(num_baldas):
    z_pos = (i + 1) * espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_total, fondo_total, grosor_panel)
    )
    bpy.context.active_object.name = f'Balda_{i+1}'