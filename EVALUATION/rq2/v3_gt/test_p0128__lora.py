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
separacion_vertical = alto_total / (num_estantes + 1)

# --- Creación de paneles verticales ---
ancho_paneles = ancho_total - grosor_panel * 2
for i in range(2):
    pos_x = -ancho_total / 2 + grosor_panel + i * (ancho_total - 2 * grosor_panel)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(grosor_panel, profundidad_total, alto_total)
    )
    bpy.context.object.name = f"Panel_Vertical_{i+1}"

# --- Creación de estantes ---
alto_estante = separacion_vertical * num_estantes
for i in range(num_estantes + 1):
    z_pos = -alto_estante / 2 + i * separacion_vertical
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_total - 2 * grosor_panel, profundidad_total, grosor_panel)
    )
    bpy.context.object.name = f"Estante_{i+1}"