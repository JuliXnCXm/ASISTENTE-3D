import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=3,
    ancho=18.0,
    fondo=14.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Sala de máquinas sobre el techo del edificio
sala_maquinas = A.crear_habitacion(
    nombre="SalaMaquinas",
    ancho=3.0,
    fondo=4.0,
    alto=3.0,
    origen=(18.0 / 2 - 1.5, 14.0 / 2 - 2.0, 9.0),
    material_muro="Muro_Pintura_Gris",
    material_suelo="Concreto_Piso",
    material_techo="Hormigon"
)