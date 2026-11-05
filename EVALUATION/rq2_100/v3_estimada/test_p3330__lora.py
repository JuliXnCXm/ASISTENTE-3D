import blender_arch as A
A.limpiar_escena()

# 1. Suelo de Terraza
suelo = A.crear_piso('Suelo_Terraza', ancho=12, fondo=10, espesor=0.15, material='Madera_Deck')

# 2. Pérgola de Acero
A.crear_columna('P_P1', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(-5, -5, 0), material='Acero_Inox')
A.crear_columna('P_P2', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(5, -5, 0), material='Acero_Inox')
A.crear_columna('P_P3', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(-5, 5, 0), material='Acero_Inox')
A.crear_columna('P_P4', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(5, 5, 0), material='Acero_Inox')
A.crear_losa_rectangular('Viga_Pergola', ancho=10, fondo=10, espesor=0.2, origen=(-5, -5, 2.8), material='Acero_Inox')

# 3. Jardineras Perimetrales
for i in range(4):
    x = -5 + i * 3
    A.crear_losa_rectangular(f'Jardinera_{i}', ancho=2.5, fondo=0.5, espesor=0.4, origen=(x, -5, 0), material='Hormigon')
    A.crear_losa_rectangular(f'Vegetacion_{i}', ancho=2.0, fondo=0.3, espesor=0.4, origen=(x, -5, 0.4), material='Terreno')

# 4. Iluminación y Cámara
A.agregar_luz('Luz_Sol', tipo='SUN', ubicacion=(5, -5, 10), energia=3)
A.crear_camara('Camara_Terraza', ubicacion=(0, -12, 5), rotacion=(80, 0, 0))