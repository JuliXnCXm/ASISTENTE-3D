import blender_arch as A
A.limpiar_escena()
ancho_edificio = 15.0
fondo_edificio = 10.0
alto_piso = 3.0
num_pisos = 4
grosor_muro = 0.3
grosor_losa = 0.2
ancho_ventana = 1.5
alto_ventana = 1.8
ancho_baranda = 1.2
alto_baranda = 1.0
ancho_puerta = 1.0
alto_puerta = 2.2
ancho_escalera = 1.1
alto_escalera = 2.8
num_puertas = 8
num_ventanas = 24
num_barandas = 24
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Calle', pisos=num_pisos, ancho=ancho_edificio, fondo=fondo_edificio, alto_piso=alto_piso, grosor_muro=grosor_muro, grosor_losa=grosor_losa, material_muro='Muro_Pintura', material_losa='Hormigon')
for i in range(num_pisos):
    for j in range(4):
        x = j * (ancho_edificio / 4)
        y = (i + 1) * (fondo_edificio / 4)
        A.abrir_vanos_batch_rectangulares(edificio, centros_world=[(x, y, alto_piso / 2)], ancho=ancho_ventana, alto=alto_ventana)
        A.crear_ventana(nombre=f'Ventana_{i}_{j}', ancho=ancho_ventana, alto=alto_ventana, prof_marco=grosor_muro, origen=(x, y, 0), material_marco='Marco_Blanco', material_vidrio='Vidrio')
for i in range(num_pisos):
    for j in range(4):
        x = j * (ancho_edificio / 4)
        y = (i + 1) * (fondo_edificio / 4)
        A.crear_baranda_lineal(nombre=f'Baranda_{i}_{j}', largo=ancho_baranda, altura=alto_baranda, origen=(x - ancho_baranda / 2, y, alto_piso), material='Acero_Inox')
for i in range(num_pisos):
    for j in range(2):
        x = j * (ancho_edificio / 4)
        y = (i + 1) * (fondo_edificio / 4)
        A.abrir_vanos_batch_rectangulares(edificio, centros_world=[(x, y, alto_piso / 2)], ancho=ancho_puerta, alto=alto_puerta)
        A.crear_puerta(nombre=f'Puerta_{i}_{j}', ancho=ancho_puerta, alto=alto_puerta, prof_marco=grosor_muro, origen=(x, y, 0), material_panel='Madera_Roble', material_marco='Marco_Negro')
A.crear_losa_rectangular('Garaje', ancho=ancho_edificio, fondo=2.0, espesor=4.0, origen=(-ancho_edificio / 2, -2.0, -4.0), material='Concreto_Piso')
A.crear_losa_rectangular('Escalera', ancho=ancho_escalera, fondo=1.0, espesor=alto_piso, origen=(ancho_edificio / 2 - ancho_escalera / 2, 0, 0), material='Hormigon')
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(5, -10, 10), energia=2.5)
A.crear_camara('Camara_Frontal', ubicacion=(-15, -10, 8), rotacion=(70, 0, 0))