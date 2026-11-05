import blender_arch as A
A.limpiar_escena()

# Crear el terreno de la parcela
A.crear_terreno_plano(
    nombre="Jardin_Casa",
    ancho=25.0,
    fondo=20.0,
    espesor=0.3,
    origen=(0, 0, -0.15),
    material="Cesped"
)

# Construir la casa en el centro del terreno
A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    grosor_muro=0.2,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    origen=(-5, -4, 0),
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Añadir árboles al jardín
A.crear_arbol_simple(nombre="Arbol_Delantero", radio_copa=2.5, altura_copa=4.0, altura_tronco=2.2, origen=(8, 5, 0))
A.crear_arbol_simple(nombre="Arbol_Trasero", radio_copa=2.0, altura_copa=3.5, altura_tronco=1.8, origen=(-9, -7, 0))