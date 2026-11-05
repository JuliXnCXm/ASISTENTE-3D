import blender_arch as A
A.limpiar_escena()

# Deck perimetral
A.crear_losa_rectangular('Deck', ancho=12, fondo=10, espesor=0.15, origen=(0,0,-0.15), material='Madera_Roble')

# Piscina interior con borde infinito
A.extruir_con_huecos(
    nombre='Piscina',
    contorno=[(-5, -4), (5, -4), (5, 4), (-5, 4)],
    agujeros=[[(-4, -4), (4, -4), (4, 4), (-4, 4)]],
    altura=1.5,
    material='Ceramica_Piso'
)

# Escalones de obra
A.crear_losa_rectangular('Escalera_Izq', ancho=1.5, fondo=0.5, espesor=0.15, origen=(-6, -4.25, 0), material='Hormigon')
A.crear_losa_rectangular('Escalera_Der', ancho=1.5, fondo=0.5, espesor=0.15, origen=(6, -4.25, 0), material='Hormigon')