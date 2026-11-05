import blender_arch as A

A.limpiar_escena()

# Crear la base de la escena
A.crear_terreno_plano(
    nombre="Parcela",
    ancho=20,
    fondo=15,
    espesor=0.2,
    material="Cesped"
)

# Definir dimensiones de la casa
ancho_casa = 10.0
fondo_casa = 8.0
alto_piso = 2.8
grosor_muro = 0.2

# Crear la casa
A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=ancho_casa,
    fondo=fondo_casa,
    alto_piso=alto_piso,
    grosor_muro=grosor_muro,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    origen=(0, 0, 0),
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Añadir elementos de jardín
A.crear_arbol_simple(
    nombre="Arbol_1",
    radio_copa=1.5,
    altura_copa=3.0,
    altura_tronco=1.5,
    origen=(-4, -3, 0)
)

A.crear_arbol_simple(
    nombre="Arbol_2",
    radio_copa=1.2,
    altura_copa=2.5,
    altura_tronco=1.2,
    origen=(4, 2, 0)
)