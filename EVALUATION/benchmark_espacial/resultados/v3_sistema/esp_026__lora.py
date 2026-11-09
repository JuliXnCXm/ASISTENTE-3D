import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Corporativo', pisos=3, ancho=12.0, fondo=10.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
anexo = A.crear_edificio_n_pisos(nombre='Anexo_Oficinas', pisos=1, ancho=4.0, fondo=3.0, alto_piso=3.0, grosor_muro=0.25, origen=(8.0, -5.0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')