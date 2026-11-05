import blender_arch as A
A.limpiar_escena()

# 1. Crear la base de la terraza
A.crear_losa_rectangular('Losa_Terraza', ancho=8, fondo=6, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')

# 2. Crear el deck de madera
A.crear_losa_rectangular('Deck_Madera', ancho=7.8, fondo=5.8, espesor=0.15, origen=(0.1, 0.1, 0.2), material='Madera_Roble')

# 3. Jardineras de obra en el perímetro
for i in range(4):
    x = -3 + i * 2
    A.crear_muro(f'Jardinera_{i}', largo=2, alto=0.9, grosor=0.15, origen=(x, -3, 0), material='Hormigon')
    A.crear_muro(f'Jardinera_{i}_2', largo=2, alto=0.9, grosor=0.15, origen=(-3, x, 0), material='Hormigon')

# 4. Pérgola de metal
A.crear_techo_plano('Pergola_Techo', ancho=2.5, fondo=2.5, espesor=0.1, origen=(-2.5, -2.5, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_1', seccion='rect', ancho=0.2, fondo=0.2, alto=0.2, origen=(-2.4, -2.4, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_2', seccion='rect', ancho=0.2, fondo=0.2, alto=0.2, origen=(2.4, -2.4, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_3', seccion='rect', ancho=0.2, fondo=0.2, alto=0.2, origen=(-2.4, 2.4, 0.2), material='Acero_Inox')
A.crear_columna('Pergola_Columna_4', seccion='rect', ancho=0.2, fondo=0.2, alto=0.2, origen=(2.4, 2.4, 0.2), material='Acero_Inox')

# 5. Mobiliario exterior
A.crear_sofa('Sofa_Exterior', ancho=2.0, fondo=0.9, origen=(-1.5, -1.5, 0.2), material='Madera')
A.agregar_tabla('Tabla_Exterior', ancho=1.2, fondo=0.6, alto=0.75, origen=(0, -1.5, 0.2), material_tablero='Madera')
A.crear_arbol_simple('Arbol_1', origen=(-3, -3, 0.2))
A.crear_arbol_simple('Arbol_2', origen=(3, -3, 0.2))
A.crear_arbol_simple('Arbol_3', origen=(-3, 3, 0.2))
A.crear_arbol_simple('Arbol_4', origen=(3, 3, 0.2))