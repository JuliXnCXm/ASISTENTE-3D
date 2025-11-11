import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones comunes
fondo = 0.9
altura_asiento = 0.45
altura_respaldo = 0.4
espesor_respaldo = 0.15

# Dimensiones específicas
largo1 = 2.0
largo2 = 1.8

# --- Módulo 1 (Eje X) ---
# Base
bpy.ops.mesh.primitive_cube_add(
    location=(largo1 / 2, fondo / 2, altura_asiento / 2),
    scale=(largo1, fondo, altura_asiento)
)
# Respaldo
bpy.ops.mesh.primitive_cube_add(
    location=(largo1 / 2, espesor_respaldo / 2, altura_asiento + altura_respaldo / 2),
    scale=(largo1, espesor_respaldo, altura_respaldo)
)

# --- Módulo 2 (Eje Y) ---
largo2_real = largo2 - fondo
# Base
bpy.ops.mesh.primitive_cube_add(
    location=(largo1 - fondo / 2, fondo + largo2_real / 2, altura_asiento / 2),
    scale=(fondo, largo2_real, altura_asiento)
)
# Respaldo
bpy.ops.mesh.primitive_cube_add(
    location=(largo1 - espesor_respaldo/2, fondo + largo2_real / 2, altura_asiento + altura_respaldo / 2),
    scale=(espesor_respaldo, largo2_real, altura_respaldo)
)