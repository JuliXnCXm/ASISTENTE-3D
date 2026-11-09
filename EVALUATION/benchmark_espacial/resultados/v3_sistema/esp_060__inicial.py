import blender_arch as A

A.limpiar_escena()

# Edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=5,
    ancho=18.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Volumen sobre la cubierta
volumen_solar = A.crear_volumen(
    nombre="Volumen_Solar",
    ancho=5.0,
    fondo=4.0,
    alto=2.5,
    origen=(18.0 / 2 - 2.5, 12.0 / 2 - 2.0, 3.0 * 5),
    material="Marco_Aluminio"
)