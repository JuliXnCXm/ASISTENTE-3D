import blender_arch as A
A.limpiar_escena()
A.crear_edificio_n_pisos(nombre='EdificioPrincipal', pisos=4, ancho=16.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(0, 0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
A.crear_edificio_n_pisos(nombre='EdificioSecundario', pisos=1, ancho=9.0, fondo=7.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(10.0, -7.0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')