import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho_nave = 30.0
fondo_nave = 20.0
alto_nave = 8.0
grosor_muro = 0.4
grosor_losa = 0.3
separacion_columnas = 6.0

# Crear muros perimetrales
muro_frente = A.crear_muro('Muro_Frente', largo=ancho_nave, alto=alto_nave, grosor=grosor_muro, origen=(0, 0, 0), material='Hormigon')
muro_fondo = A.crear_muro('Muro_Fondo', largo=ancho_nave, alto=alto_nave, grosor=grosor_muro, origen=(0, fondo_nave - grosor_muro, 0), material='Hormigon')
muro_izq = A.crear_muro('Muro_Izq', largo=fondo_nave, alto=alto_nave, grosor=grosor_muro, origen=(0, 0, 0), rotacion_z=90, material='Hormigon')
muro_der = A.crear_muro('Muro_Der', largo=fondo_nave, alto=alto_nave, grosor=grosor_muro, origen=(ancho_nave - grosor_muro, 0, 0), rotacion_z=90, material='Hormigon')

# Crear columnas
num_columnas_x = int(ancho_nave / separacion_columnas) + 1
num_columnas_y = int(fondo_nave / separacion_columnas) + 1

for i in range(num_columnas_x):
    for j in range(num_columnas_y):
        x_pos = i * separacion_columnas - ancho_nave/2 + separacion_columnas/2
        z_pos = alto_nave/2
        A.crear_columna(f'Columna_{i}_{j}', seccion='rect', ancho=0.5, fondo=0.5, alto=alto_nave, origen=(x_pos, 0, z_pos), material='Acero_Inox')

# Crear losa de cubierta
losa_cubierta = A.crear_losa_rectangular('Losa_Cubierta', ancho=ancho_nave, fondo=fondo_nave, espesor=grosor_losa, origen=(0, 0, alto_nave), material='Hormigon')