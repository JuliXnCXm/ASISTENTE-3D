import blender_arch as A

A.limpiar_escena()

# Dimensiones generales
ancho_total = 18.0
fondo_total = 16.0
alto_piso = 3.0
num_pisos = 4
grosor_muro = 0.25

# Dimensiones de los brazos
ancho_brazo_x = 6.0
ancho_brazo_y = 6.0
fondo_brazo_x = fondo_total - ancho_brazo_y
fondo_brazo_y = ancho_total - ancho_brazo_x

# Crear muros para el brazo en X
muro_ext_x1 = A.crear_muro('Muro_Exterior_X1', largo=ancho_brazo_x, alto=num_pisos * alto_piso, grosor=grosor_muro, origen=(0, fondo_brazo_y, 0), rotacion_z=90)
muro_int_x1 = A.crear_muro('Muro_Interior_X1', largo=ancho_brazo_x, alto=num_pisos * alto_piso, grosor=grosor_muro, origen=(0, 0, 0), rotacion_z=90)

# Crear muros para el brazo en Y
muro_ext_y1 = A.crear_muro('Muro_Exterior_Y1', largo=ancho_brazo_y, alto=num_pisos * alto_piso, grosor=grosor_muro, origen=(ancho_brazo_x, 0, 0), rotacion_z=0)
muro_int_y1 = A.crear_muro('Muro_Interior_Y1', largo=ancho_brazo_y, alto=num_pisos * alto_piso, grosor=grosor_muro, origen=(ancho_brazo_x, fondo_brazo_y, 0), rotacion_z=0)

# Unir todos los muros en un solo objeto
muros_l = [muro_ext_x1, muro_int_x1, muro_ext_y1, muro_int_y1]
A.unir_objetos(muros_l, nombre='Edificio_L')