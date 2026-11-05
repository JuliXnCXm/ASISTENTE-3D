import blender_arch as A
A.limpiar_escena()
A.crear_techo_plano(nombre='TechoPlano', ancho=6.0, fondo=4.0, espesor=0.2, caida_x=0.0, caida_y=0.0, origen=(0, 0, 3.0), material='Hormigon')
A.crear_terreno_plano(nombre='Deck', ancho=5.5, fondo=3.5, espesor=0.15, origen=(0, 0, 3.2), material='Madera_Roble')
for i in range(4):
    x0 = -1.5 if i % 2 == 0 else 1.5
    y0 = -1.5 if i < 2 else 1.5
    A.crear_muro(f'Jardinera_{i}', largo=3.0, alto=0.8, grosor=0.15, origen=(x0, y0, 3.2), material='Ladrillo_Blanco')
A.crear_muro('Pergola_Fondo', largo=3.0, alto=2.5, grosor=0.1, origen=(-1.5, -1.5, 3.2), material='Acero_Inox')
A.crear_muro('Pergola_Lateral', largo=3.0, alto=2.5, grosor=0.1, origen=(-1.5, 1.5, 3.2), material='Acero_Inox')
A.crear_columna('Pilastra_1', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(-1.4, -1.4, 3.2), material='Acero_Inox')
A.crear_columna('Pilastra_2', seccion='rect', ancho=0.1, fondo=0.1, alto=2.5, origen=(1.4, -1.4, 3.2), material='Acero_Inox')
A.crear_sofa('Sofa_Exterior', ancho=2.0, fondo=0.9, origen=(-0.5, 0.5, 3.2), material='Madera')
A.crear_mesa('Mesa_Exterior', ancho=1.2, fondo=0.7, alto=0.7, origen=(0.5, 0.5, 3.2), material_tablero='Madera')
A.crear_arbol_simple('Arbol_0', radio_copa=0.5, altura_copa=2.0, altura_tronco=1.5, origen=(-1.5, -1.5, 3.2))
A.crear_arbol_simple('Arbol_1', radio_copa=0.5, altura_copa=2.0, altura_tronco=1.5, origen=(-1.5, 1.5, 3.2))
A.crear_arbol_simple('Arbol_2', radio_copa=0.5, altura_copa=2.0, altura_tronco=1.5, origen=(1.5, -1.5, 3.2))
A.crear_arbol_simple('Arbol_3', radio_copa=0.5, altura_copa=2.0, altura_tronco=1.5, origen=(1.5, 1.5, 3.2))