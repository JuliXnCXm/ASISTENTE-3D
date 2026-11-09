import blender_arch as A

A.limpiar_escena()

# Edificio principal
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=6,
    ancho=10.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)

# Anexo adosado a la fachada frontal
anexo_x = 10.0 - 4.0 # Centrado en X
anexo_y = 0.25 # Pegado al muro
anexo_z = 0.0 # En el suelo del piso inferior

A.crear_habitacion(
    nombre="Anexo_Estudio",
    ancho=4.0,
    fondo=4.0,
    alto=3.0,
    origen=(anexo_x, anexo_y, anexo_z),
    material_muro="Muro_Pintura_Gris",
    material_suelo="Porcelanato"
)