import blender_arch as A
A.limpiar_escena()

# 1. Crear la base de la terraza
A.crear_losa_rectangular('Base_Terraza', ancho=8, fondo=7, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')

# 2. Crear el deck de madera
A.crear_losa_rectangular('Deck_Madera', ancho=7.8, fondo=6.8, espesor=0.15, origen=(0.1,0.1,0.2), material='Madera_Roble')

# 3. Jardineras de obra en el perímetro
for i in range(4):
    x = -3 + i * 2
    A.crear_muro(f'Jardinera_{i}', largo=2, alto=0.9, grosor=0.15, origen=(x, -3, 0), material='Hormigon')
    A.crear_muro(f'Jardinera_{i}_2', largo=2, alto=0.9, grosor=0.15, origen=(x, -3, 0), rotacion_z=90, material='Hormigon')

# 4. Pérgola de metal en una esquina
A.crear_losa_rectangular('Pergola_Base', ancho=2.5, fondo=2.5, espesor=0.1, origen=(-2.5, -2.5, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_1', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(-2.4, -2.4, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_2', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(2.4, -2.4, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_3', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(-2.4, 2.4, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_4', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(2.4, 2.4, 0.2), material='Acero_Inox')
A.crear_losa_rectangular('Pergola_Techo', ancho=2.4, fondo=2.4, espesor=0.1, origen=(-2.3, -2.3, 2.5), material='Acero_Inox')

# 5. Mobiliario exterior
A.crear_sofa('Sofa_Exterior', ancho=2.0, origen=(-1.5, 1.5, 0.2), material='Madera_Nogal')
A.crear_mesa('Mesa_Exterior', ancho=1.2, fondo=0.6, alto=0.7, origen=(0, 0, 0.2), material_tablero='Madera_Roble', material_patas='Acero_Inox')

# 6. Vegetación
for i in range(15):
    x = -2 + i * 1.5
    A.crear_arbol_simple(f'Arbol_{i}', radio_copa=0.5, altura_copa=2.0, altura_tronco=1.5, origen=(x, 2, 0.2))