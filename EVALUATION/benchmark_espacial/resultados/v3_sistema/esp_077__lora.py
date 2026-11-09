import blender_arch as A
A.limpiar_escena()
A.crear_edificio_n_pisos(nombre='Edificio_Circular', pisos=3, ancho=14.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, origen=(0, 0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
A.girar_objecto('Edificio_Circular', -50, 'Z')