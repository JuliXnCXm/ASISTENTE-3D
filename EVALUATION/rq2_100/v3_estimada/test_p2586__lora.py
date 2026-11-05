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

# --- Creación de Baldas ---
espacio_entre_baldas = (alto - grosor_panel) / (num_baldas - 1)

for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + grosor_panel / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho, profundidad, grosor_panel)
    )
    bpy.context.object.name = f"Balda_{i+1}"

# --- Creación de Paneles laterales ---
ancho_panel = ancho - 2 * grosor_panel
pos_x_lateral = ancho_panel / 2

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-pos_x_lateral, 0, alto / 2),
    scale=(grosor_panel, profundidad, alto)
)
bpy.context.object.name = "Panel_Izquierdo"

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(pos_x_lateral, 0, alto / 2),
    scale=(grosor_panel, profundidad, alto)
)
bpy.context.object.name = "Panel_Derecho"