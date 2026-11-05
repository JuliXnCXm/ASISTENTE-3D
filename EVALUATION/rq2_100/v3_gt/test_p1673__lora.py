import blender_arch as A
A.limpiar_escena()

# Terreno base
terreno = A.crear_terreno_plano(
    nombre="Parcela",
    ancho=20,
    fondo=15,
    espesor=0.3,
    origen=(0, 0, -0.15),
    material="Cesped"
)

# Casa centrada en el terreno
casa = A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=8.0,
    fondo=6.0,
    alto_piso=2.8,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    origen=(-4, -3, 0),
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Vegetación
A.crear_arbol_simple(
    nombre="Arbol_1",
    radio_copa=2.0,
    altura_copa=3.5,
    altura_tronco=2.0,
    origen=(-5, 4, 0)
)
A.crear_arbol_simple(
    nombre="Arbol_2",
    radio_copa=1.5,
    altura_copa=2.5,
    altura_tronco=1.5,
    origen=(5, -3, 0)
)
A.crear_arbol_simple(
    nombre="Arbol_3",
    radio_copa=1.2,
    altura_copa=2.0,
    altura_tronco=1.2,
    origen=(-3, -5, 0)
)