import blender_arch as A
A.limpiar_escena()

# Crear la estructura de la cocina en L
ancho_cocina = 5.0
fondo_cocina = 4.0
alto_muro = 2.7

# Muros
muro_frente = A.crear_muro('Muro_Frente', largo=ancho_cocina, alto=alto_muro, origen=(0, 0, 0), material='Muro_Pintura_Gris')
muro_fondo = A.crear_muro('Muro_Fondo', largo=fondo_cocina, alto=alto_muro, origen=(0, fondo_cocina, 0), rotacion_z=90, material='Muro_Pintura_Gris')
muro_izq = A.crear_muro('Muro_Izquierdo', largo=fondo_cocina, alto=alto_muro, origen=(0, 0, 0), rotacion_z=-90, material='Muro_Pintura_Gris')
muro_der = A.crear_muro('Muro_Derecho', largo=ancho_cocina, alto=alto_muro, origen=(ancho_cocina, 0, 0), rotacion_z=90, material='Muro_Pintura_Gris')

# Piso
piso = A.crear_piso('Piso_Cocina', ancho=ancho_cocina + fondo_cocina, fondo=4.0, espesor=0.02, origen=(0, 0, 0), material='Porcelanato')

# Isla central
ancho_isla = 1.8
fondo_isla = 0.9
alto_isla = 0.9
origen_isla = (ancho_cocina / 2, fondo_cocina / 2, 0)

# Encimera de la isla
encimera_isla = A.crear_losa_rectangular('Encimera_Isla', ancho=ancho_isla, fondo=fondo_isla, espesor=0.04, origen=(origen_isla[0], origen_isla[1], alto_isla), material='Madera_Roble')

# Base de la isla
base_isla = A.crear_losa_rectangular('Base_Isla', ancho=ancho_isla, fondo=fondo_isla, espesor=0.6, origen=(origen_isla[0], origen_isla[1], alto_isla - 0.6), material='Madera_Roble')

# Fregadero integrado
ancho_fregadero = 0.5
fondo_fregadero = 0.4
alto_fregadero = 0.9
origen_fregadero = (ancho_isla / 2, fondo_isla / 2, alto_isla)
A.crear_losa_rectangular('Fregadero', ancho=ancho_fregadero, fondo=fondo_fregadero, espesor=0.01, origen=(origen_fregadero[0], origen_fregadero[1], alto_isla), material='Acero_Inox')

# Luces colgantes
num_luces = 3
for i in range(num_luces):
    pos_x = ancho_isla / 2 + 0.5 + i * 0.8
    pos_y = fondo_isla / 2 + 0.5
    pos_z = alto_isla + 0.8
    A.agregar_luz(f'Luz_{i}', tipo='POINT', ubicacion=(pos_x, pos_y, pos_z), energia=100, color=(1, 0.9, 0.8))