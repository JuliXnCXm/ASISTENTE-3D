import blender_arch as A
A.limpiar_escena()
edificio_1 = A.crear_edificio_n_pisos(nombre='Edificio_Central', pisos=3, ancho=18.0, fondo=10.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(0, 0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
edificio_2 = A.crear_edificio_n_pisos(nombre='Edificio_Sur', pisos=1, ancho=6.0, fondo=7.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(6.0 + 0.25, 7.0 / 2, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')