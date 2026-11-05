import blender_arch as A
A.limpiar_escena()

# Parcela exterior
A.crear_terreno_plano(
    nombre="Parcela",
    ancho=25.0,
    fondo=20.0,
    espesor=0.3,
    material="Cesped"
)

# Casa interior
A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=12.0,
    fondo=9.0,
    alto_piso=2.8,
    origen=(0, 0, 0.15),
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Vegetación
A.crear_arbol_simple(
    nombre="Arbol_Izquierdo",
    radio_copa=2.0,
    altura_copa=3.5,
    altura_tronco=2.0,
    origen=(-6, 7, 0.15)
)
A.crear_arbol_simple(
    nombre="Arbol_Derecho",
    radio_copa=2.0,
    altura_copa=3.5,
    altura_tronco=2.0,
    origen=(6, -5, 0.15)
)