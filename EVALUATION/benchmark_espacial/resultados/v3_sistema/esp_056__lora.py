import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=3,
    ancho=16.0,
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
    ancho=5.0,
    fondo=3.0,
    alto=2.5,
    origen=(8.0, 7.0, 9.0), # Centrada sobre el techo del edificio (8.0, 7.0) a Z=3.0
    material_muro="Metal",
    material_suelo="Concreto_Piso",
    material_techo="Acero_Inox"
)