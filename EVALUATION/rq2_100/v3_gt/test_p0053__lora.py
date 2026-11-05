import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 1.8
ancho_total = 0.8
profundidad_total = 0.3
num_estantes = 5
grosor_panel = 0.02

# --- Creación de los paneles verticales ---
ancho_paneles = ancho_total / 2
pos_x_paneles = [-ancho_paneles, ancho_paneles]

for pos_x in pos_x_paneles:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(grosor_panel, profundidad_total, alto_total)
    )
    bpy.context.object.name = f"PanelVertical_{pos_x:.2f}"

# --- Creación de los estantes ---
espacio_entre_estantes = alto_total / (num_estantes + 1)

for i in range(num_estantes):
    altura_estante = i * espacio_entre_estantes + (i + 1) * espacio_entre_estantes / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, altura_estante),
        scale=(ancho_total, grosor_panel, grosor_panel)
    )
    bpy.context.object.name = f"Estante_{i+1}"