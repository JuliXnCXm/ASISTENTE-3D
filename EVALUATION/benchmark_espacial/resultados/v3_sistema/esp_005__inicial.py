import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=4,
    ancho=10.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Balcon en voladizo
A.crear_losa_rectangular(
    nombre="Balcon_Trasero",
    ancho=10.0,
    fondo=1.5,
    espesor=0.2,
    origen=(0, -8.0 + 0.25, 9.0), # Origen en el centro del muro trasero del piso 3
    material="Hormigon"
)

# Baranda en la fachada trasera
A.crear_baranda_lineal(
    nombre="Baranda_Balcon",
    largo=10.0,
    altura=1.0,
    poste_cada=1.2,
    origen=(-5.0, -8.0 + 0.25, 9.0),
    material="Acero_Inox"
)