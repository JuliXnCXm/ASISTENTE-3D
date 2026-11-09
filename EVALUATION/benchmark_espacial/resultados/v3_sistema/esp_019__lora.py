import blender_arch as A

A.limpiar_escena()

# Crear el edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=5,
    ancho=20.0,
    fondo=14.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Calcular la posición para la marquesina
ancho_total_edificio = 20.0
fondo_total_edificio = 14.0
altura_piso_suelo = 3.0
pos_x_marquesina = (ancho_total_edificio / 2) - (4.0 / 2) - 1.0 # Centrar en el muro trasero, con un pequeño margen

# Crear la marquesina
A.crear_losa_rectangular(
    nombre="Marquesina_Sur",
    ancho=4.0,
    fondo=1.5,
    espesor=0.2,
    origen=(pos_x_marquesina, fondo_total_edificio / 2, altura_piso_suelo + 3.0),
    material="Acero_Inox"
)