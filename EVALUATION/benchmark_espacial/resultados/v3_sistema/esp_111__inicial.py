import blender_arch as A

A.limpiar_escena()

# Dimensiones generales
ancho_total = 16.0
fondo_total = 16.0
alto_piso = 3.0
num_pisos = 3
grosor_muro = 0.25

# Dimensiones brazos
ancho_brazo_x = 6.0
fondo_brazo_y = 7.0

# Crear muros para el brazo en X
muro_norte_x = A.crear_muro('Muro_Norte_X', largo=ancho_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(0, fondo_total - grosor_muro/2, 0), rotacion_z=90)
muro_sur_x = A.crear_muro('Muro_Sur_X', largo=ancho_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(0, grosor_muro/2, 0), rotacion_z=90)

# Crear muros para el brazo en Y
muro_oeste_y = A.crear_muro('Muro_Oeste_Y', largo=fondo_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(grosor_muro/2, 0, 0), rotacion_z=90)
muro_este_y = A.crear_muro('Muro_Este_Y', largo=fondo_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(ancho_total - grosor_muro/2, 0, 0), rotacion_z=90)

# Unir todos los muros en un solo objeto
edificio_l = A.unir_objetos([muro_norte_x, muro_sur_x, muro_oeste_y, muro_este_y], nombre='Edificio_L')