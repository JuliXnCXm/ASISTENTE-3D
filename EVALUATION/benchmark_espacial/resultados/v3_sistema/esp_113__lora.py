import blender_arch as A

A.limpiar_escena()

# Dimensiones generales
ancho_total = 16.0
fondo_total = 14.0
alto_piso = 3.0
num_pisos = 3

# Dimensiones de los brazos
ancho_brazo_x = 7.0
fondo_brazo_y = 7.0

# Crear el primer brazo (en eje X)
A.crear_muro(nombre="Muro_Norte", largo=ancho_total, alto=alto_piso * num_pisos, origen=(0, fondo_brazo_y, 0), rotacion_z=90)
A.crear_muro(nombre="Muro_Sur", largo=ancho_total, alto=alto_piso * num_pisos, origen=(0, 0, 0), rotacion_z=-90)

# Crear el segundo brazo (en eje Y)
A.crear_muro(nombre="Muro_Oeste", largo=fondo_brazo_y, alto=alto_piso * num_pisos, origen=(ancho_brazo_x, 0, 0), rotacion_z=90)
A.crear_muro(nombre="Muro_Este", largo=fondo_brazo_y, alto=alto_piso * num_pisos, origen=(ancho_total, 0, 0), rotacion_z=-90)