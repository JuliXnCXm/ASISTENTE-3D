import blender_arch as A

A.limpiar_escena()

# Edificio principal
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=6,
    ancho=10.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Muro_Pintura_Gris"
)

# Anexo adosado al norte
anexo = A.crear_edificio_n_pisos(
    nombre="Anexo_Oficinas",
    pisos=1,
    ancho=5.0,
    fondo=4.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    origen=(0, 8.0 - 0.25, 0), # Origen en el centro del muro sur del edificio principal
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Muro_Pintura_Gris"
)