import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas tipo
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=4,
    ancho=14.0,
    fondo=14.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)

# Marquesina en voladizo
ancho_marquesina = 4.0
vuelo_marquesina = 1.5
altura_marquesina = 3.0

A.crear_losa_rectangular(
    nombre="Marquesina",
    ancho=ancho_marquesina,
    fondo=vuelo_marquesina,
    espesor=0.2,
    origen=(0, -14.0 + vuelo_marquesina / 2, altura_marquesina),
    material="Acero_Inox"
)