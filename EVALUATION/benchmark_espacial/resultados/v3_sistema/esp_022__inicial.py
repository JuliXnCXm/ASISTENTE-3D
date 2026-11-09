import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Central', pisos=4, ancho=12.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
anexo_x = 12.0 - 5.0
anexo_y = 12.0 / 2 + 4.0
A.crear_edificio_n_pisos(nombre='Anexo', pisos=1, ancho=5.0, fondo=4.0, alto_piso=3.0, grosor_muro=0.25, origen=(anexo_x, anexo_y, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')