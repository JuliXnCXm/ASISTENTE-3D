import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho = 0.8
alto = 1.8
profundidad = 0.3
num_baldas = 4

# --- Creación de los componentes ---
# Paneles laterales
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(ancho / 2 * i, 0, alto / 2),
        scale=(ancho * abs(i), profundidad, alto)
    )
    bpy.context.object.name = f"Panel_Lateral_{i}"

# Baldas
espacio_entre_baldas = alto / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho, profundidad, 0.05)
    )
    bpy.context.object.name = f"Bala_{i+1}"