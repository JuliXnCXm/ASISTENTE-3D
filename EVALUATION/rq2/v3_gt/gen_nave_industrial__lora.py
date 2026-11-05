import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho = 30.0
fondo = 20.0
alto = 8.0
grosor_muro = 0.4
grosor_losa = 0.3
separacion_columna = 6.0

# Crear muros perimetrales
muro_frente = A.crear_muro('Muro_Frente', largo=ancho, alto=alto, grosor=grosor_muro, origen=(0,0,0), material='Hormigon')
muro_fondo = A.crear_muro('Muro_Fondo', largo=ancho, alto=alto, grosor=grosor_muro, origen=(0,fondo-grosor_muro,0), material='Hormigon')
muro_izq = A.crear_muro('Muro_Izq', largo=fondo, alto=alto, grosor=grosor_muro, origen=(0,0,0), rotacion_z=90, material='Hormigon')
muro_der = A.crear_muro('Muro_Der', largo=fondo, alto=alto, grosor=grosor_muro, origen=(ancho-grosor_muro,0,0), rotacion_z=90, material='Hormigon')

# Crear columnas
num_columnas_x = ancho // separacion_columna + 1
num_columnas_y = fondo // separacion_columna + 1

for i in range(num_columnas_x):
    for j in range(num_columnas_y):
        x = i * separacion_columna - (ancho / 2)
        z = alto / 2
        A.crear_columna(f'Columna_{i}_{j}', seccion='rect', ancho=0.5, fondo=0.5, alto=alto, origen=(x, grosor_muro/2, z), material='Acero_Inox')

# Crear losa de cubierta
losa_cubierta = A.crear_losa_rectangular('Losa_Cubierta', ancho=ancho, fondo=fondo, espesor=grosor_losa, origen=(0,0,alto), material='Hormigon')