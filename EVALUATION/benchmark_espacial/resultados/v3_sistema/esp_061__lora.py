import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=6,
    ancho=20.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Sala de máquinas sobre el techo del edificio
sala_x = 20.0 / 2 - 5.0 / 2
sala_y = 12.0 / 2 - 4.0 / 2
A.crear_habitacion(
    nombre="SalaMaquinas",
    ancho=5.0,
    fondo=4.0,
    alto=2.5,
    origen=(sala_x, sala_y, 3.0),
    material_muro="Muro_Pintura_Gris",
    material_suelo="Concreto_Piso",
    material_techo="Hormigon"
)