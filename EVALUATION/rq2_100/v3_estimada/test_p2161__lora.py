import blender_arch as A
A.limpiar_escena()

# Deck de madera
A.crear_losa_rectangular('Deck', ancho=10, fondo=10, espesor=0.15, origen=(0,0,-0.15), material='Madera_Roble')

# Piscina principal
A.crear_losa_rectangular('Agua_Piscina', ancho=6, fondo=4, espesor=1.5, origen=(0,0,0), material='Agua')

# Borde infinito en el lado largo
borde_infinito = A.crear_losa_rectangular('Borde_Infinito', ancho=6, fondo=0.1, espesor=1.5, origen=(0,4,0), material='Muro_Pintura_Gris')
borde_infinito.rotation_euler[2] = 1.5708 # 90 grados

# Escalones de obra
A.crear_losa_rectangular('Escalera_1', ancho=1.5, fondo=0.5, espesor=0.15, origen=(-1.5, 0.25, 0), material='Hormigon')
A.crear_losa_rectangular('Escalera_2', ancho=1.5, fondo=0.5, espesor=0.15, origen=(-1.5, 0.75, 0.15), material='Hormigon')
A.crear_losa_rectangular('Escalera_3', ancho=1.5, fondo=0.5, espesor=0.15, origen=(-1.5, 1.25, 0.3), material='Hormigon')
A.crear_losa_rectangular('Escalera_4', ancho=1.5, fondo=0.5, espesor=0.15, origen=(-1.5, 1.75, 0.45), material='Hormigon')