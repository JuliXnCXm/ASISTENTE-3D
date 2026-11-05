import blender_arch as A
A.limpiar_escena()

# 1. Suelo de deck
A.crear_piso('Deck_Terraza', ancho=8, fondo=7, espesor=0.15, material='Madera_Deck')

# 2. Pérgola
A.crear_losa_rectangular('Losa_Pergola', ancho=6, fondo=4, espesor=0.2, origen=(1, 1, 0.15), material='Hormigon')
A.crear_barra('Pergola_Soportes_1', largo=6, alto=2.5, origen=(-3, 2, 0.15), material='Acero_Inox')
A.crear_barra('Pergola_Soportes_2', largo=6, alto=2.5, origen=(3, 2, 0.15), material='Acero_Inox')
A.crear_barra('Pergola_Cubierta_1', largo=6, alto=0.2, origen=(-3, 2, 2.5), material='Acero_Inox')
A.crear_barra('Pergola_Cubierta_2', largo=6, alto=0.2, origen=(3, 2, 2.5), material='Acero_Inox')
A.crear_barra('Pergola_Cubierta_3', largo=4, alto=0.2, origen=(0, 2, 2.5), material='Acero_Inox')

# 3. Jardineras perimetrales
for i in range(4):
    x = -3 + i * 2
    A.crear_losa_rectangular(f'Jardinera_{i}', ancho=0.5, fondo=0.5, espesor=0.3, origen=(x, 2.25, 0.15), material='Concreto_Piso')
    A.crear_planta(f'Vegetacion_{i}', radio=0.2, altura=0.5, origen=(x, 2.25, 0.45))

# 4. Iluminación y cámara
A.agregar_luz('Luz_Sol', tipo='SUN', ubicacion=(5, -5, 10), energia=2.5)
A.crear_camara('Camara_Terraza', ubicacion=(0, -8, 3), rotacion=(80, 0, 0))