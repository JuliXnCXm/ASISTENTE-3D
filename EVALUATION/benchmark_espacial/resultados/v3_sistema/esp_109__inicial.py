import blender_arch as A
A.limpiar_escena()
ancho_total = 20.0
fondo_total = 14.0
alto_piso = 3.0
num_pisos = 4
grosor_muro = 0.3
ancho_brazo_x = 7.0
fondo_brazo_y = 8.0
ancho_efectivo = ancho_brazo_x - grosor_muro
fondo_efectiva = fondo_brazo_y + grosor_muro
A.crear_edificio_n_pisos(nombre='Edificio_L_Norte', pisos=num_pisos, ancho=ancho_efectivo, fondo=fondo_efectiva, alto_piso=alto_piso, origen=(0, 0, 0))
ancho_efectivo = fondo_brazo_y - grosor_muro
fondo_efectiva = ancho_brazo_x + grosor_muro
A.crear_edificio_n_pisos(nombre='Edificio_L_Sur', pisos=num_pisos, ancho=ancho_efectivo, fondo=fondo_efectiva, alto_piso=alto_piso, origen=(ancho_efectivo, 0, 0))