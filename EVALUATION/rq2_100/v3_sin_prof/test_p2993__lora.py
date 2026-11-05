import blender_arch as A

A.limpiar_escena()

# Crear la losa base de la plaza
A.crear_losa_rectangular(
    nombre="Losa_Plaza",
    ancho=15.0,
    fondo=15.0,
    espesor=0.2,
    origen=(0, 0, 0),
    material="Concreto_Piso"
)

# Colocar un banco en el centro
A.crear_sofa(
    nombre="Banco_Central",
    ancho=2.0,
    fondo=0.6,
    alto_asiento=0.45,
    origen=(0, 0, 0.2),
    material="Madera_Roble"
)

# Añadir árboles en las esquinas
A.crear_arbol_simple(
    nombre="Arbol_NE",
    radio_copa=1.8,
    altura_copa=3.0,
    altura_tronco=1.5,
    origen=(-4, 4, 0.2)
)
A.crear_arbol_simple(
    nombre="Arbol_NO",
    radio_copa=1.8,
    altura_copa=3.0,
    altura_tronco=1.5,
    origen=(4, 4, 0.2)
)
A.crear_arbol_simple(
    nombre="Arbol_SE",
    radio_copa=1.8,
    altura_copa=3.0,
    altura_tronco=1.5,
    origen=(-4, -4, 0.2)
)
A.crear_arbol_simple(
    nombre="Arbol_SO",
    radio_copa=1.8,
    altura_copa=3.0,
    altura_tronco=1.5,
    origen=(4, -4, 0.2)
)