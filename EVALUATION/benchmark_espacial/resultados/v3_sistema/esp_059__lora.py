import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=3,
    ancho=12.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Sala de máquinas sobre el techo del edificio
sala_maquinas = A.crear_habitacion(
    nombre="SalaMaquinas",
    ancho=4.0,
    fondo=3.0,
    alto=3.0,
    origen=(6.0, 5.0, 9.0), # Origen en el centro del techo del edificio (x=12/2, y=10/2, z=3*3)
    material_muro="Muro_Pintura_Gris",
    material_suelo="Concreto_Piso",
    material_techo="Hormigon"
)