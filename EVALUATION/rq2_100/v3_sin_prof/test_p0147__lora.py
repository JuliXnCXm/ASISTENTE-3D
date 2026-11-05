import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 1.8
ancho_total = 1.0
fondo_total = 0.3
num_estantes = 5
grosor_panel = 0.02

# --- Creación de los paneles principales ---
ancho_util = ancho_total - grosor_panel * 2
fondo_util = fondo_total - grosor_panel * 2

# Panel trasero
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, fondo_util / 2, alto_total / 2),
    scale=(ancho_total, grosor_panel, alto_total)
)
bpy.context.object.name = "PanelTrasero"

# Panel frontal
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, -fondo_util / 2, alto_total / 2),
    scale=(ancho_total, grosor_panel, alto_total)
)
bpy.context.object.name = "PanelFrontal"

# Paneles laterales
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * (ancho_util / 2) + grosor_panel/2, 0, alto_total / 2),
        scale=(grosor_panel, fondo_util, alto_total)
    )
    bpy.context.object.name = f"PanelLateral_{i}"

# --- Creación de los estantes ---
espacio_entre_estantes = alto_total / (num_estantes - 1)

for i in range(num_estantes):
    altura_estante = i * espacio_entre_estantes
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, altura_estante),
        scale=(ancho_util, fondo_total, grosor_panel)
    )
    bpy.context.object.name = f"Estante_{i+1}"