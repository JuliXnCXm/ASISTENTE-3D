import blender_arch as A

A.limpiar_escena()

# Dimensiones generales
ancho_total = 18.0
fondo_total = 16.0
alto_piso = 3.0
num_pisos = 2
grosor_muro = 0.3

# Dimensiones brazos
ancho_brazo_x = 6.0
fondo_brazo_y = 8.0
ancho_brazo_y = fondo_brazo_y # Brazo en Y es el mismo ancho que en X

# Crear muros
muro_norte = A.crear_muro('Muro_Norte', largo=ancho_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(0, fondo_total - grosor_muro/2, 0), rotacion_z=90)
muro_sur = A.crear_muro('Muro_Sur', largo=ancho_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(0, grosor_muro/2, 0), rotacion_z=-90)
muro_este = A.crear_muro('Muro_Este', largo=fondo_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(ancho_total - grosor_muro/2, 0, 0), rotacion_z=0)
muro_oeste = A.crear_muro('Muro_Oeste', largo=fondo_total, alto=alto_piso * num_pisos, grosor=grosor_muro, origen=(grosor_muro/2, 0, 0), rotacion_z=180)

# Abrir huecos para la esquina vacía
A.abrir_vanos_batch_rectangulares(muro_norte, centros_world=[(ancho_brazo_x/2, fondo_brazo_y, alto_piso/2)], ancho=ancho_brazo_x, alto=ancho_brazo_y)
A.abrir_vanos_batch_rectangulares(muro_este, centros_world=[(ancho_brazo_x, fondo_brazo_y/2, alto_piso/2)], ancho=ancho_brazo_y, alto=ancho_brazo_x)

# Crear pisos
for i in range(num_pisos):
    z_piso = i * alto_piso
    A.crear_piso(f"Piso_{i+1}", ancho=ancho_total, fondo=fondo_total, espesor=0.3, origen=(0, 0, z_piso))