import bpy
import math

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
diametro_tabla = 0.8
altura_mesa = 0.45
grosor_tabla = 0.04
diametro_pata = 0.05
num_patas = 3

# --- Creación de la tabla superior ---
radio_tabla = diametro_tabla / 2
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_tabla,
    depth=grosor_tabla,
    location=(0, 0, altura_mesa - grosor_tabla / 2)
)
bpy.context.object.name = 'Tabla_Mesa'

# --- Creación de las patas ---
altura_pata = altura_mesa - grosor_tabla
radio_pata = diametro_pata / 2
radio_distribucion_patas = radio_tabla * 0.7

for i in range(num_patas):
    angulo = i * (2 * math.pi / num_patas)
    pos_x = radio_distribucion_patas * math.cos(angulo)
    pos_y = radio_distribucion_patas * math.sin(angulo)
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radio_pata,
        depth=altura_pata,
        location=(pos_x, pos_y, altura_pata / 2)
    )
    bpy.context.object.name = f'Pata_{i+1}'