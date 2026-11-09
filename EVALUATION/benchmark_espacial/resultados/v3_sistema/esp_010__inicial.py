import blender_arch as A

A.limpiar_escena()

# Edificio principal
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=4,
    ancho=18.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Muro_Pintura_Gris"
)

# Anexo adosado al lado oeste
anexo = A.crear_edificio_n_pisos(
    nombre="Anexo_Oficinas",
    pisos=1,
    ancho=6.0,
    fondo=4.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    origen=(18.0 - 0.25, 0, 0), # X = 18.0 para que toque el muro del edificio
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Muro_Pintura_Gris"
)