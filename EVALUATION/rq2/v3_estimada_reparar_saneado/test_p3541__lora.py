import blender_arch as A
A.limpiar_escena()
A.crear_piso('Deck_Terraza', ancho=8, fondo=6, espesor=0.15, material='Madera')
A.crear_losa_rectangular('Losa_Pergola', ancho=8, fondo=6, espesor=0.2, origen=(0, 0, -0.1), material='Hormigon')
A.crear_barra('Pergola_Sureste', largo=8, alto=2.5, origen=(-4, 3, 0.2), material='Acero_Inox')
A.crear_barra('Pergola_Suroeste', largo=8, alto=2.5, origen=(4, 3, 0.2), material='Acero_Inox')
A.crear_barra('Pergola_Noreste', largo=6, alto=2.5, origen=(-4, 0, 0.2), material='Acero_Inox')
A.crear_barra('Pergola_Noroeste', largo=6, alto=2.5, origen=(4, 0, 0.2), material='Acero_Inox')
for i in range(4):
    A.crear_losa_rectangular(f'Jardinera_{i}', ancho=1.5, fondo=0.5, espesor=0.3, origen=(-4 + i * 2, 3, 0.2), material='Concreto_Piso')
    A.crear_arbol_simple(f'Vegetacion_{i}', radio_copa=0.7, altura_copa=1.2, altura_tronco=0.5, origen=(-4 + i * 2, 3, 0.5))
A.agregar_luz('Luz_Sol', tipo='SUN', ubicacion=(5, -5, 10), energia=3)
A.crear_camara('Camara_Terraza', ubicacion=(0, -10, 5), rotacion=(80, 0, 0))