import blender_arch as A
import math

A.limpiar_escena()

# Crear la habitación
hab = A.crear_habitacion(
    nombre="Dormitorio", 
    ancho=4.0, 
    fondo=3.5, 
    alto=2.7, 
    grosor_muro=0.15, 
    material_muro="Muro_Pintura_Gris", 
    material_suelo="Parquet"
)

# Posicionar la cama contra la pared del fondo
cama = A.crear_cama(
    nombre="Cama_Doble", 
    ancho=1.6, 
    largo=2.0, 
    origen=(2.0, 0.15, 0), 
    material_colchon="Textil_Blanco", 
    material_base="Madera"
)

# Posicionar el armario en la pared izquierda
armario = A.crear_armario(
    nombre="Armario", 
    ancho=1.8, 
    alto=2.4, 
    fondo=0.6, 
    num_puertas=2, 
    origen=(0.15, 1.75, 0), 
    material_cuerpo="MDF_Blanco"
)
armario.rotation_euler[2] = math.radians(90)