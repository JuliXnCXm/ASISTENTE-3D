import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 1.8
ancho_total = 1.0
fondo_total = 0.3
num_baldas = 5
grosor_panel = 0.02

# --- Creación de componentes ---
# Paneles verticales
ancho_panel_v = ancho_total / 2
pos_x_v = [ancho_panel_v, -ancho_panel_v]
for x in pos_x_v:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, 0, alto_total / 2),
        scale=(grosor_panel, fondo_total, alto_total)
    )
    bpy.context.object.name = f"Panel_V_{x:.2f}"

# Baldas
espacio_entre_baldas = alto_total / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_total, fondo_total, grosor_panel)
    )
    bpy.context.object.name = f"Bala_{i+1}"