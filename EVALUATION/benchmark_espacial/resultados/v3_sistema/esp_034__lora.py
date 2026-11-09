import blender_arch as A

A.limpiar_escena()

# Edificio principal
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioPrincipal",
    pisos=3,
    ancho=14.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)

# Anexo
anexo = A.crear_edificio_n_pisos(
    nombre="Anexo",
    pisos=1,
    ancho=6.0,
    fondo=3.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    origen=(7.0, -3.25, 0), # Centrado en la fachada frontal del edificio principal
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)