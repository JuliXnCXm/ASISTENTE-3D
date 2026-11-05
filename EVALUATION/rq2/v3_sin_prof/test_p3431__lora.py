import blender_arch as A
A.limpiar_escena()

# Crear la estructura de la cocina en L
ancho_cocina = 4.0
fondo_cocina = 5.0
alto_muro = 2.8

# Muros perimetrales
muro_frente = A.crear_muro('Muro_Frente', largo=ancho_cocina, alto=alto_muro, origen=(0, fondo_cocina, 0), rotacion_z=90)
muro_fondo = A.crear_muro('Muro_Fondo', largo=ancho_cocina, alto=alto_muro, origen=(0, 0, 0), rotacion_z=-90)
muro_izq = A.crear_muro('Muro_Izq', largo=fondo_cocina, alto=alto_muro, origen=(0, 0, 0), rotacion_z=0)
muro_der = A.crear_muro('Muro_Der', largo=fondo_cocina, alto=alto_muro, origen=(ancho_cocina, 0, 0), rotacion_z=180)

# Piso y techo
piso = A.crear_piso('Piso_Cocina', ancho=ancho_cocina + 1.0, fondo=fondo_cocina + 1.0, espesor=0.05, origen=(-0.5, -0.5, 0), material='Porcelanato')
techo = A.crear_techo_plano('Techo_Cocina', ancho=ancho_cocina + 1.0, fondo=fondo_cocina + 1.0, espesor=0.2, origen=(-0.5, -0.5, alto_muro), material='Yeso')

# Muebles bajos y altos
ancho_modulo = 0.6
fondo_modulo = 0.6
alto_modulo = 0.85
grosor_encimera = 0.04

# Muebles bajos
for i in range(3):
    x_pos = i * (ancho_modulo + 0.1) + 0.5
    y_pos = fondo_cocina - 0.1
    A.crear_armario(f'Mueble_Bajo_{i}', ancho=ancho_modulo, alto=alto_modulo, fondo=fondo_modulo, num_puertas=1, origen=(x_pos, y_pos, 0), material_cuerpo='MDF_Blanco')

# Encimera
encimera_bajos = A.crear_losa_rectangular('Encimera_Bajos', ancho=ancho_cocina, fondo=fondo_cocina, espesor=grosor_encimera, origen=(0, 0, alto_modulo), material='Cuarzo_Blanco')

# Muebles altos
for i in range(3):
    x_pos = i * (ancho_modulo + 0.1) + 0.5
    y_pos = fondo_cocina - 0.1
    A.crear_armario(f'Mueble_Alto_{i}', ancho=ancho_modulo, alto=alto_modulo, fondo=fondo_modulo, num_puertas=1, origen=(x_pos, y_pos, alto_modulo + 0.4), material_cuerpo='MDF_Blanco')

# Isla central
ancho_isla = 2.0
fondo_isla = 1.0
alto_isla = alto_modulo + 0.4
origen_isla = (ancho_cocina / 2, 0.5, alto_isla)
A.crear_losa_rectangular('Isla_Central', ancho=ancho_isla, fondo=fondo_isla, espesor=alto_isla, origen=origen_isla, material='Concreto_Piso')

# Taburetes
for i in range(2):
    x_taburete = origen_isla[0] + 0.5 + i * 0.8
    y_taburete = 0.5
    z_taburete = alto_isla + 0.45
    A.crear_silla(f'Taburete_{i}', ancho=0.4, fondo=0.4, alto_asiento=0.45, origen=(x_taburete, y_taburete, z_taburete), material='Acero_Inox')

# Iluminación y cámara
A.agregar_luz('Luz_Principal', tipo='AREA', ubicacion=(ancho_cocina/2, fondo_cocina/2, alto_muro+2), energia=800)
A.crear_camara('Camara_Cocina', ubicacion=(ancho_cocina/2, -3, alto_muro), rotacion=(75, 0, 0))