import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y SUELO ---
A.crear_losa_rectangular('Losa_Terraza', ancho=10, fondo=8, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')
A.crear_piso('Deck_Madera', ancho=9.8, fondo=7.8, espesor=0.05, origen=(0,0,0.2), material='Madera_Roble')

# --- JARDINERAS PERIMETRALES ---
for i in range(4):
    x = -4 + i * 3
    A.crear_losa_rectangular(f'Ladrillo_{i}', ancho=2.5, fondo=0.2, espesor=0.1, origen=(x, -3.5, 0.2), material='Hormigon')
    A.crear_planta_simple(f'Vegetacion_{i}', radio_copa=0.6, altura_copa=1.2, altura_tronco=0.4, origen=(x, -3.5, 0.3))

# --- PÉRGOLA METÁLICA ---
A.crear_barra('Pergola_Principal_1', largo=9.8, alto=2.8, origen=(-4.9, 3.9, 0.2), material='Acero_Inox')
A.crear_barra('Pergola_Principal_2', largo=9.8, alto=2.8, origen=(-4.9, -3.9, 0.2), material='Acero_Inox')
A.crear_barra('Pergola_Principal_3', largo=2.5, alto=2.8, origen=(-4.9, 0, 0.2), material='Acero_Inox')
A.crear_barra('Pergola_Principal_4', largo=2.5, alto=2.8, origen=(4.9, 0, 0.2), material='Acero_Inox')

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('Luz_Sol', tipo='SUN', ubicacion=(5, -5, 10), energia=3)
A.crear_camara('Camara_Terraza', ubicacion=(0, -10, 5), rotacion=(80, 0, 0))