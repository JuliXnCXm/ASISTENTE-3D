import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=6,
    ancho=18.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Sala de máquinas sobre el techo
ancho_sala = 3.0
fondo_sala = 3.0
alto_sala = 2.5
z_cubierta = 3.0 * 6 # Altura del último piso

A.crear_habitacion(
    nombre="SalaMaquinas",
    ancho=ancho_sala,
    fondo=fondo_sala,
    alto=alto_sala,
    origen=(0, 0, z_cubierta),
    material_muro="Muro_Pintura_Gris",
    material_suelo="Concreto_Piso",
    material_techo="Hormigon"
)