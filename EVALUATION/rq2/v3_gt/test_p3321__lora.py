import blender_arch as A
A.limpiar_escena()

# 1. Suelo de la terraza
A.crear_piso('Suelo_Terraza', ancho=10, fondo=6, espesor=0.15, material='Madera_Deck')

# 2. Pérgola de acero
A.crear_techo_rectangular('Pergola_Cubierta', ancho=8, fondo=4, alto=2.5, origen=(1, 1, 0.15), material='Acero_Inox')
A.crear_columna('Poste_Pergola_1', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(-0.5, -0.5, 0.15), material='Acero_Inox')
A.crear_columna('Poste_Pergola_2', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(9.5, -0.5, 0.15), material='Acero_Inox')
A.crear_columna('Poste_Pergola_3', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(-0.5, 5.5, 0.15), material='Acero_Inox')
A.crear_columna('Poste_Pergola_4', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(9.5, 5.5, 0.15), material='Acero_Inox')

# 3. Jardineras y vegetación
for i in range(4):
    A.crear_columna(f'Jardinera_{i}', seccion='rect', ancho=0.5, fondo=0.5, alto=0.4, origen=(i*2.5 + 1, 0.5, 0.15), material='Hormigon')
    A.crear_planta(f'Vegetacion_{i}', nombre=f'Arbol_{i}', radio_copa=0.7, altura_copa=2.0, altura_tronco=1.5, origen=(i*2.5 + 1, 0.5, 0.15))

# 4. Mobiliario de exterior
A.crear_sofa('Sofa_Terraza', ancho=2.0, fondo=0.9, origen=(3, 3, 0.15), material='Tela_Gris')
A.crear_mesa('Mesa_Exterior', ancho=1.2, fondo=0.7, alto=0.7, origen=(3, 4.5, 0.15), material_tablero='Madera_Roble')