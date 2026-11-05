import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA Y ZONA COMÚN ---
casa = A.crear_casa_n_pisos(
    nombre="Casa",
    pisos=1,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_tejado=True,
    altura_cumbrera=1.5,
    voladizo=0.4,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# --- HABITACIONES CONCREAS ---
hab1 = A.crear_habitacion(
    nombre="SalaComedor",
    ancho=5.0,
    fondo=4.0,
    alto=3.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_suelo=True,
    con_techo=True,
    origen=(-2.5, 2.0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)
hab2 = A.crear_habitacion(
    nombre="Dormitorio",
    ancho=4.0,
    fondo=5.0,
    alto=3.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_suelo=True,
    con_techo=True,
    origen=(3.0, 2.5, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)
hab3 = A.crear_habitacion(
    nombre="Baño",
    ancho=2.5,
    fondo=2.5,
    alto=3.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_suelo=True,
    con_techo=True,
    origen=(7.5, 0.5, 0),
    material_muro="Muro_Pintura",
    material_suelo="Porcelanato",
    material_techo="Yeso"
)

# --- MOBILIARIO ESSENCIAL ---
# Sala-Comedor
A.crear_mesa(
    nombre="MesaPrincipal",
    ancho=2.0,
    fondo=1.0,
    alto=0.75,
    origen=(-1.5, 1.5, 0),
    material_tablero="Madera_Roble"
)
A.crear_silla(
    nombre="Silla1",
    origen=(-1.5, 1.0, 0),
    material="Madera_Roble"
)
A.crear_silla(
    nombre="Silla2",
    origen=(-0.5, 1.0, 0),
    material="Madera_Roble"
)
A.crear_silla(
    nombre="Silla3",
    origen=(0.5, 1.0, 0),
    material="Madera_Roble"
)
A.crear_silla(
    nombre="Silla4",
    origen=(1.5, 1.0, 0),
    material="Madera_Roble"
)

# Dormitorio
A.crear_cama(
    nombre="CamaDormitorio",
    ancho=1.6,
    largo=2.0,
    origen=(3.2, 2.2, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)

# Baño
A.crear_mesa(
    nombre="MesaBaño",
    ancho=0.8,
    fondo=0.6,
    alto=0.8,
    origen=(7.5, 1.2, 0),
    material_tablero="MDF_Blanco"
)