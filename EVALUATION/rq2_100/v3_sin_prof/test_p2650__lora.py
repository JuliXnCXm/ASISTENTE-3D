import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 1.8
ancho_total = 1.2
fondo_total = 0.3
num_estantes = 4
grosor_panel = 0.02

# --- Creación de los paneles principales ---
# Panel frontal
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_total / 2),
    scale=(ancho_total, grosor_panel, alto_total)
)
panel_frontal = bpy.context.active_object
panel_frontal.name = "Panel_Frontal"

# Panel trasero
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_total / 2),
    scale=(ancho_total, grosor_panel, alto_total)
)
panel_trasero = bpy.context.active_object
panel_trasero.name = "Panel_Trasero"
panel_trasero.location.z = -alto_total

# Panel izquierdo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho_total/2 + grosor_panel/2, 0, alto_total / 2),
    scale=(grosor_panel, fondo_total, alto_total)
)
panel_izquierdo = bpy.context.active_object
panel_izquierdo.name = "Panel_Izquierdo"

# Panel derecho
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho_total/2 - grosor_panel/2, 0, alto_total / 2),
    scale=(grosor_panel, fondo_total, alto_total)
)
panel_derecho = bpy.context.active_object
panel_derecho.name = "Panel_Derecho"
panel_derecho.location.z = -alto_total

# --- Creación de los estantes ---
espacio_util = alto_total - grosor_panel * 2
separacion = espacio_util / (num_estantes + 1)

for i in range(num_estantes):
    altura_estante = grosor_panel + separacion * (i + 1)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, altura_estante),
        scale=(ancho_total - 2 * grosor_panel, fondo_total, grosor_panel)
    )
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1}"