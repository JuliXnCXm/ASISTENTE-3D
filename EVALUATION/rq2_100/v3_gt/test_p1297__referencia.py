import blender_arch as A
A.limpiar_escena()

ancho_parcela = 25.0
fondo_parcela = 20.0
ancho_casa = 12.0
fondo_casa = 9.0

A.crear_terreno_plano(
    nombre="Parcela_Residencial",
    ancho=ancho_parcela,
    fondo=fondo_parcela,
    espesor=0.3,
    origen=(0, 0, -0.15),
    material="Cesped"
)

origen_casa_x = -ancho_casa / 2
origen_casa_y = -fondo_casa / 2
A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=ancho_casa,
    fondo=fondo_casa,
    alto_piso=2.8,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    origen=(origen_casa_x, origen_casa_y, 0),
    material_muro="Ladrillo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

A.crear_arbol_simple(
    nombre="Arbol_Frontal_1",
    radio_copa=2.0,
    altura_copa=3.0,
    altura_tronco=1.8,
    origen=(8, -7, 0)
)

A.crear_arbol_simple(
    nombre="Arbol_Frontal_2",
    radio_copa=1.8,
    altura_copa=2.5,
    altura_tronco=1.5,
    origen=(-8, -6, 0)
)

A.agregar_luz(
    nombre="Sol",
    tipo="SUN",
    ubicacion=(-10, -15, 20),
    energia=3.0
)