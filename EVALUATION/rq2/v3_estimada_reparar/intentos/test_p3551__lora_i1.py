import blender_arch as A
A.limpiar_escena()
A.crear_losa_rectangular('Base_Terraza', ancho=12, fondo=8, espesor=0.2, origen=(0, 0, -0.2), material='Concreto_Piso')
A.crear_losa_rectangular('Deck_Madera', ancho=10, fondo=6, espesor=0.15, origen=(0, 0, 0.2), material='Madera_Roble')
for i in range(4):
    x = -4 + i * 3
    A.crear_muro(f'Jardinera_{i}', largo=3, alto=0.9, grosor=0.15, origen=(x, -4, 0.2), material='Hormigon')
    A.crear_muro(f'Jardinera_{i}_largo', largo=3, alto=0.9, grosor=0.15, origen=(-4, x, 0.2), material='Hormigon')
A.crear_losa_rectangular('Pergola_Base', ancho=2.5, fondo=2.5, espesor=0.1, origen=(-2, -2, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_1', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(-2.2, -2.2, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_2', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(2.2, -2.2, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_3', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(-2.2, 2.2, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_4', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(2.2, 2.2, 0.2), material='Acero_Inox')
A.crear_losa_rectangular('Pergola_Techo', ancho=2.1, fondo=2.1, espesor=0.1, origen=(-2.1, -2.1, 2.5), material='Acero_Inox')
A.crear_sofa('Sofa_Exterior', ancho=2.0, origen=(-1, 1, 0.2), material='Madera')
A.crear_mesa('Mesa_Exterior', ancho=1.2, fondo=0.6, alto=0.7, origen=(0, 0, 0.2), material_tablero='Madera')