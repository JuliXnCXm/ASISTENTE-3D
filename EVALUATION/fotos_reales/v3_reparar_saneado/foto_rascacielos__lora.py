import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='TorreCorporativa', pisos=25, ancho=16.0, fondo=16.0, alto_piso=3.7, grosor_muro=0.25, grosor_losa=0.3, ventanas_fachada=True, ventana_ancho=2.0, ventana_alto=2.2, ventana_alfeizar=0.2, ventana_separacion=3.0, material_muro='Muro_Pintura_Gris', material_losa='Hormigon', material_vidrio='Vidrio_Templado', material_marco='Marco_Aluminio', origen=(0, 0, 0))
A.crear_arbol_simple('Arbol_Plaza', radio_copa=2.5, altura_copa=4.0, altura_tronco=2.2, origen=(-10, -10, 0))
A.crear_sofa('Sofa_Area', ancho=2.5, fondo=0.9, origen=(10, -8, 0), material='Cuero')
A.crear_mesa('Mesa_Area', ancho=1.2, fondo=0.7, alto=0.45, origen=(10, 0, 0), material_tablero='Madera_Nogal')
A.crear_coche('Carro1', origen=(-5, -5, 0), rotacion=(75, 0, 0))
A.crear_coche('Carro2', origen=(5, -5, 0), rotacion=(30, 0, 0))