import blender_arch as A
A.limpiar_escena()
A.crear_escalera_recta(nombre='EscaleraPrincipal', huella=0.28, contrahuella=0.175, ancho=1.1, num_peldanos=14, grosor_peldano=0.03, con_contrahuellas=True, con_zancas=True, espesor_zanca=0.15, origen=(0, 0, 0), material='Hormigon')
A.crear_edificio_n_pisos(nombre='EdificioConEscalera', pisos=2, ancho=12.0, fondo=15.0, alto_piso=2.8, grosor_muro=0.2, grosor_losa=0.2, con_columnas=True, seccion_columna='rect', dim_columna=(0.4, 0.4), modulo_columna_x=4.0, modulo_columna_y=5.0, origen=(-6, -7.5, 0))