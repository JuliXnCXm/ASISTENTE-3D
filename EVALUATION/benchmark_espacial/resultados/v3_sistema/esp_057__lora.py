import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=6,
    ancho=10.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Cuarto técnico sobre la cubierta
A.crear_habitacion(
    nombre="CuartoTecnico",
    ancho=5.0,
    fondo=3.0,
    alto=3.0,
    origen=(5.0, 5.0, 6.0),
    material_muro="Muro_Pintura_Gris",
    material_suelo="Concreto_Piso",
    material_techo="Hormigon"
)