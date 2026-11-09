import blender_arch as A
A.limpiar_escena()
A.crear_edificio_n_pisos(nombre='EdificioPrincipal', pisos=6, ancho=20.0, fondo=10.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(0, 0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
A.crear_edificio_n_pisos(nombre='EdificioSecundario', pisos=1, ancho=8.0, fondo=6.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(-5, -4, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')