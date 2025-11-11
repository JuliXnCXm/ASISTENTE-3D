import bpy
import math

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del cerramiento ---
ancho_total = 5.0
alto_total = 3.0
ancho_lama = 0.10
espesor_lama = 0.03
separacion_lamas = 0.05
angulo_rotacion_rad = math.radians(45)

# --- Bucle de creación de lamas ---
paso = ancho_lama + separacion_lamas
num_lamas = int(ancho_total / paso)

for i in range(num_lamas):
    # Calcular posición X de cada lama
    pos_x = -ancho_total / 2 + paso / 2 + i * paso
    
    # Crear la lama en su posición
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(espesor_lama, ancho_lama, alto_total),
        rotation=(0, 0, angulo_rotacion_rad)
    )
    lama = bpy.context.active_object
    lama.name = f"Lama.{i+1:03d}"