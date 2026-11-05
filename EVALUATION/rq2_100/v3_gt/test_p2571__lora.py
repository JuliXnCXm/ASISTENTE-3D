import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho = 1.2
alto = 2.0
fondo = 0.3
num_baldas = 5
grosor_panel = 0.02

# --- Creación de baldas ---
espacio_entre_baldas = (alto - grosor_panel) / (num_baldas - 1)

for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + grosor_panel / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho, fondo, grosor_panel)
    )
    bpy.context.object.name = f"Balda_{i+1}"