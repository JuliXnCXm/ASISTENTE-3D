import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho = 1.2
alto = 1.8
profundidad = 0.3
num_estantes = 5
grosor_panel = 0.02

# --- Creación de los paneles verticales ---
for i in range(2):
    loc_x = -ancho / 2 + grosor_panel / 2 + i * (ancho - 2 * grosor_panel) / (num_estantes - 1)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(loc_x, 0, alto / 2),
        scale=(grosor_panel, profundidad, alto)
    )
    bpy.context.object.name = f"Panel_Vertical_{i+1}"

# --- Creación de los estantes ---
espacio_entre_estantes = alto / (num_estantes - 1)
for i in range(num_estantes):
    z_pos = i * espacio_entre_estantes
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho - 2 * grosor_panel, profundidad, grosor_panel)
    )
    bpy.context.object.name = f"Estante_{i+1}"