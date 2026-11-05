import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho_total = 1.2
alto_total = 1.8
profundidad_total = 0.3
num_estantes = 5
grosor_panel = 0.02

# --- Creación de los paneles verticales ---
ancho_paneles = (ancho_total / num_estantes) * (num_estantes - 1)
for i in range(num_estantes):
    pos_x = -ancho_total / 2 + ancho_paneles / 2 + i * (ancho_paneles / (num_estantes - 1))
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(grosor_panel, profundidad_total, alto_total)
    )
    bpy.context.object.name = f"Panel_Vertical_{i}"

# --- Creación de los estantes ---
espacio_entre_estantes = alto_total / (num_estantes - 1)
for i in range(num_estantes):
    pos_z = -alto_total / 2 + grosor_panel / 2 + i * espacio_entre_estantes
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, pos_z),
        scale=(ancho_total, profundidad_total, grosor_panel)
    )
    bpy.context.object.name = f"Estante_{i}"