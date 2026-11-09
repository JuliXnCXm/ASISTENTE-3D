import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Corporativo', pisos=5, ancho=18.0, fondo=8.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
ancho_efectivo = 18.0 - 2 * 0.25
pos_x_marquesina = ancho_efectivo / 2 - 2
altura_marquesina_suelo = 3.0 + 1.5
A.crear_losa_rectangular(nombre='Marquesina_Acceso', ancho=4.0, fondo=1.5, espesor=0.2, origen=(pos_x_marquesina, 0, altura_marquesina_suelo), material='Acero_Inox')