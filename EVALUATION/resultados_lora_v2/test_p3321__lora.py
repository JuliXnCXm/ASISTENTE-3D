import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y suelo ---
A.crear_losa_rectangular('Losa_Terraza', ancho=10, fondo=8, espesor=0.2, origen=(0, 0, -0.2), material='Concreto_Piso')
A.crear_piso('Deck_Terraza', ancho=9.5, fondo=7.5, espesor=0.05, origen=(0, 0, 0.2), material='Madera')

# --- Jardineras perimetrales ---
for i in range(4):
    x = (i % 2) * 3.5 - 3.5
    y = (i // 2) * 3.5 - 3.5
    A.crear_losa_rectangular(f'Jardinera_{i}', ancho=1.5, fondo=0.6, espesor=0.4, origen=(x, y, 0.2), material='Hormigon')
    A.crear_planta_simple(f'Vegetacion_{i}', radio_copa=0.8, altura_copa=1.2, altura_tronco=0.4, origen=(x + 0.75, y + 0.3, 0.6))

# --- Pérgola de Acero ---
A.crear_techo_plano('Pergola_Cubierta', ancho=9.5, fondo=7.5, espesor=2.5, origen=(-4.75, -3.75, 0.2), material='Acero_Inox')
A.crear_columna('Pila_Pergola_1', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(-4.7, -3.7, 0.2), material='Acero_Inox')
A.crear_columna('Pila_Pergola_2', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(4.7, -3.7, 0.2), material='Acero_Inox')
A.crear_columna('Pila_Pergola_3', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(-4.7, 3.7, 0.2), material='Acero_Inox')
A.crear_columna('Pila_Pergola_4', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(4.7, 3.7, 0.2), material='Acero_Inox')

# --- Mobiliario Exterior ---
A.crear_sofa('Sofa_Exterior', ancho=2.5, fondo=0.9, origen=(0, -2.5, 0.2), material='Tela_Gris')
A.crear_mesa('Mesa_Exterior', ancho=1.2, fondo=0.6, alto=0.7, origen=(0, 0, 0.2), material_tablero='Madera_Roble')