import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=5,
    ancho=20.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Balcon en la fachada Norte (lado largo)
A.crear_losa_rectangular(
    nombre="Balcon_Norte",
    ancho=20.0,
    fondo=3.0,
    espesor=0.25,
    origen=(0, -12.0 + 0.25/2, 4.5),
    material="Hormigon"
)

# Baranda en el borde frontal del balcón
A.crear_baranda_lineal(
    nombre="Baranda_Balcon_Norte",
    largo=20.0,
    altura=1.0,
    poste_cada=1.2,
    origen=(-10, -12.0 + 0.25, 7.5),
    material="Acero_Inox"
)