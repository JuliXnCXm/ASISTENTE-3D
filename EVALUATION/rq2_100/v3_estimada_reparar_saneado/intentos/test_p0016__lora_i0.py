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

# --- Creación de la base y estantes ---
ancho_util = ancho - grosor_panel * 2
alto_estante = alto / num_estantes

# Base
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_estante / 2),
    scale=(ancho, profundidad, alto_estante)
)
base = bpy.context.active_object
base.name = "Base_Estanteria"

# Estantes
espaciado = ancho_util / (num_estantes - 1)
for i in range(num_estantes):
    pos_x = -ancho / 2 + espaciado * i
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_estante * (i + 1)),
        scale=(ancho_util, profundidad, grosor_panel)
    )
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1}"