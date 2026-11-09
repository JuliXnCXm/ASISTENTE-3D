import blender_arch as A

A.limpiar_escena()

# Crear el edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=3,
    ancho=20.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Calcular la posición para la marquesina
ancho_marquesina = 4.0
vuelo_marquesina = 1.5
altura_marquesina = 3.0
pos_x_marquesina = - (edificio.ancho / 2) + (ancho_marquesina / 2) + vuelo_marquesina

# Crear la marquesina
A.crear_losa_rectangular(
    nombre="Marquesina_Acceso",
    ancho=ancho_marquesina,
    fondo=vuelo_marquesina,
    espesor=0.2,
    origen=(pos_x_marquesina, 0, altura_marquesina),
    material="Acero_Inox"
)