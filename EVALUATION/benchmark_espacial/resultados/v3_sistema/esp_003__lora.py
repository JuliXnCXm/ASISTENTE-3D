import blender_arch as A

A.limpiar_escena()

# Crear el edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=6,
    ancho=10.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Calcular la posición para la marquesina
ancho_total_edificio = 10.0
fondo_total_edificio = 8.0
altura_piso_suelo = 3.0 * (5 + 0.5) # 5 pisos completos + 0.5m de altura del suelo
pos_x_marquesina = ancho_total_edificio / 2 - 4.0 / 2
pos_y_marquesina = fondo_total_edificio - 0.25 # Para que quede sobre el muro

# Crear la marquesina
A.crear_losa_rectangular(
    nombre="Marquesina_Sur",
    ancho=4.0,
    fondo=1.5,
    espesor=0.2,
    origen=(pos_x_marquesina, pos_y_marquesina, altura_piso_suelo),
    material="Acero_Inox"
)