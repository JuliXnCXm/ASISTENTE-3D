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

# --- Creación de los paneles principales ---
# Panel frontal
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho_total / 2, fondo_total / 2, alto_total / 2),
    scale=(ancho_total, grosor_panel, alto_total)
)
panel_frontal = bpy.context.active_object
panel_frontal.name = "Panel_Frontal"

# Panel trasero
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho_total / 2, fondo_total / 2, alto_total / 2),
    scale=(ancho_total, grosor_panel, alto_total)
)
panel_trasero = bpy.context.active_object
panel_trasero.name = "Panel_Trasero"

# Panel izquierdo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho_total / 2, fondo_total / 2, alto_total / 2),
    scale=(grosor_panel, fondo_total, alto_total)
)
panel_izquierdo = bpy.context.active_object
panel_izquierdo.name = "Panel_Izquierdo"

# Panel derecho
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho_total / 2, fondo_total / 2, alto_total / 2),
    scale=(grosor_panel, fondo_total, alto_total)
)
panel_derecho = bpy.context.active_object
panel_derecho.name = "Panel_Derecho"

# --- Creación de las baldas ---
espacio_entre_baldas = alto_total / (num_baldas + 1)

for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + (num_baldas / 2) * espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_total - 2 * grosor_panel, fondo_total - 2 * grosor_panel, 0.04)
    )
    balda = bpy.context.active_object
    balda.name = f"Balda_{i+1}"