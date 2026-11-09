import blender_arch as A
A.limpiar_escena()
A.crear_edificio_n_pisos(nombre='Edificio_Central', pisos=4, ancho=10.0, fondo=8.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(0, 0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
A.crear_edificio_n_pisos(nombre='Edificio_Sur', pisos=1, ancho=9.0, fondo=7.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(10 + 5, -7 / 2, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')