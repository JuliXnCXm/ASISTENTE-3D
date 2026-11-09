import blender_arch as A

A.limpiar_escena()

# Edificio principal
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=4,
    ancho=18.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)

# Anexo a la fachada derecha
anexo_x = 18.0 + 5.0 # Extensión en X
anexo_y = 4.0       # Profundidad en Y
anexo_z = 3.0       # Altura en Z
anexo = A.crear_edificio_n_pisos(
    nombre="Anexo_Oficinas",
    pisos=1,
    ancho=anexo_x,
    fondo=anexo_y,
    alto_piso=anexo_z,
    grosor_muro=0.25,
    con_techo_plano=True,
    origen=(anexo_x / 2, anexo_y / 2, anexo_z / 2),
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)