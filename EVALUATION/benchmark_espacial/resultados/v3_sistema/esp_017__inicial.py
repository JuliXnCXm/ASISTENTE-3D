import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=6,
    ancho=20.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Balcon en el lado sur (frente)
A.crear_losa_rectangular(
    nombre="Balcon_Sur",
    ancho=20.0,
    fondo=1.5,
    espesor=0.2,
    origen=(0, -12.0 + 0.25, 3.0),
    material="Hormigon"
)

# Baranda en el borde del balcón
A.crear_baranda_lineal(
    nombre="Baranda_Balcon_Sur",
    largo=20.0,
    altura=1.0,
    poste_cada=1.2,
    origen=(-10.0, -12.0 + 0.25, 3.0 + 1.5),
    material="Acero_Inox"
)