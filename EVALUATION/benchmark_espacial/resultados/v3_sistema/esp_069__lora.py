import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=3,
    ancho=12.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Cuarto técnico sobre la cubierta
A.crear_habitacion(
    nombre="CuartoTecnico",
    ancho=3.0,
    fondo=4.0,
    alto=2.5,
    origen=(6.0, 6.0, 9.0), # Centrado en X e Y, sobre la losa de la cubierta (Z=9.0)
    material_muro="Muro_Pintura_Gris",
    material_suelo="Concreto_Piso",
    material_techo="Hoja_de_Teja"
)