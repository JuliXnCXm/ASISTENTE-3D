import blender_arch as A
A.limpiar_escena()
ancho_total = 20.0
fondo_total = 14.0
alto_piso = 3.0
num_pisos = 2
ancho_brazo_x = 6.0
fondo_brazo_y = 7.0
grosor_muro = 0.3
ancho_efectivo_x = ancho_total - grosor_muro
fondo_efectiva_y = fondo_brazo_y + grosor_muro
pos_x_brazo_1 = grosor_muro / 2
pos_y_brazo_1 = fondo_efectiva_y / 2
A.crear_edificio_n_pisos(nombre='Brazo_X', pisos=num_pisos, ancho=ancho_efectivo_x, fondo=fondo_efectiva_y, alto_piso=alto_piso, origen=(pos_x_brazo_1, pos_y_brazo_1, 0))
ancho_efectivo_y = ancho_brazo_x - grosor_muro
fondo_efectiva_x = fondo_brazo_y + grosor_muro
pos_x_brazo_2 = ancho_efectivo_x / 2
pos_y_brazo_2 = fondo_efectiva_x + grosor_muro
A.crear_edificio_n_pisos(nombre='Brazo_Y', pisos=num_pisos, ancho=ancho_efectivo_y, fondo=fondo_efectiva_x, alto_piso=alto_piso, origen=(pos_x_brazo_2, pos_y_brazo_2, alto_piso))