import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y SUELO ---
A.crear_losa_rectangular('Losa_Terraza', ancho=12, fondo=8, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')
A.crear_piso('Deck_Madera', ancho=12, fondo=8, espesor=0.15, origen=(0,0,0.2), material='Madera_Roble')

# --- PÉRGOLA DE ACERO ---
A.crear_columna('P_P1', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(-6, 6, 0.2), material='Acero_Inox')
A.crear_columna('P_P2', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(6, 6, 0.2), material='Acero_Inox')
A.crear_columna('P_P3', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(-6, -6, 0.2), material='Acero_Inox')
A.crear_columna('P_P4', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(6, -6, 0.2), material='Acero_Inox')
A.crear_losa_rectangular('Viga_Pergola', ancho=12, fondo=0.4, espesor=0.2, origen=(-6, 6, 2.8), material='Acero_Inox')
A.crear_losa_rectangular('Viga_Pergola_2', ancho=12, fondo=0.4, espesor=0.2, origen=(-6, -6, 2.8), material='Acero_Inox')
A.crear_losa_rectangular('Viga_Pergola_3', ancho=12, fondo=0.4, espesor=0.2, origen=(6, 6, 2.8), material='Acero_Inox')
A.crear_losa_rectangular('Viga_Pergola_4', ancho=12, fondo=0.4, espesor=0.2, origen=(6, -6, 2.8), material='Acero_Inox')

# --- MUEBLES DE JARDÍN ---
A.crear_sofa('Sofa_Jardin', ancho=2.5, fondo=0.9, origen=(0, 7, 0.2), material='Tela_Gris')
A.crear_mesa('Mesa_Jardin', ancho=1.2, fondo=0.6, alto=0.7, origen=(0, 8.5, 0.2), material_tablero='Madera')

# --- JARDINERÍAS CON VEGETACIÓN ---
for i in range(4):
    x = -6 + i * 2.5
    A.crear_losa_rectangular(f'Jardinera_{i}', ancho=1.5, fondo=1.5, espesor=0.3, origen=(x, 6, 0.2), material='Hormigon')
    A.crear_planta_simple(f'Vegetacion_{i}', radio_copa=0.8, altura_copa=1.2, altura_tronco=0.4, origen=(x, 6.75, 0.5))

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('Luz_Sol', tipo='SUN', ubicacion=(5, -5, 10), energia=2.5)
A.crear_camara('Camara_Terraza', ubicacion=(0, -10, 5), rotacion=(80, 0, 0))