import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioOficinas', pisos=6, ancho=12.0, fondo=14.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
ancho_efectivo = 12.0 - 0.25 * 2
pos_x_marquesina = ancho_efectivo / 2 + 4.0
pos_y_marquesina = 7.0
A.crear_losa_rectangular(nombre='Marquesina', ancho=4.0, fondo=1.5, espesor=0.2, origen=(pos_x_marquesina, pos_y_marquesina, 3.0), material='Acero_Inox')