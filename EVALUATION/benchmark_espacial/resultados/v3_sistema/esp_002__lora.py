import blender_arch as A

A.limpiar_escena()

# Edificio principal
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=5,
    ancho=18.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Muro_Pintura_Gris"
)

# Anexo adosado a la fachada frontal
anexo = A.crear_edificio_n_pisos(
    nombre="Anexo_Oficinas",
    pisos=1,
    ancho=6.0,
    fondo=3.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    origen=(18.0 - 6.0 / 2, 8.0 + 3.0 / 2, 0),
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Muro_Pintura_Gris"
)