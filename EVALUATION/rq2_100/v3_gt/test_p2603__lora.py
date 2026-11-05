import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho = 1.2
alto = 2.0
profundidad = 0.3
num_baldas = 5
espesor_madera = 0.02

# --- Creación de las partes ---
# Base
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto / 2))
base = bpy.context.active_object
base.name = "Base_Estanteria"
base.dimensions = (ancho, profundidad, alto)

# Baldas
espacio_entre_baldas = alto / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = espesor_madera / 2 + (i * espacio_entre_baldas) + (espesor_madera / 2)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z_pos))
    balda = bpy.context.active_object
    balda.name = f"Balda_{i+1}"
    balda.dimensions = (ancho, profundidad, espesor_madera)