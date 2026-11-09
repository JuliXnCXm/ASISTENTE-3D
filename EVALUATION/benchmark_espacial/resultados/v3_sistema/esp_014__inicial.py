import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioPrincipal', pisos=3, ancho=14.0, fondo=8.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
anexo = A.crear_edificio_n_pisos(nombre='Anexo', pisos=1, ancho=4.0, fondo=4.0, alto_piso=3.0, grosor_muro=0.25, origen=(14.0 - 0.25, 0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')