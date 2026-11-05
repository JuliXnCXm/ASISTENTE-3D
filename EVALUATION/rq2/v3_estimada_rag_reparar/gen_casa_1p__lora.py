import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la casa
casa = A.crear_casa_n_pisos(
    nombre="Casa_Principal",
    pisos=1,
    ancho=12.0,
    fondo=9.0,
    alto_piso=2.8,
    grosor_muro=0.2,
    grosor_losa=0.2,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Definir y crear las habitaciones
habitacion1 = A.crear_habitacion(
    nombre="Habitacion_1",
    ancho=5.0,
    fondo=4.0,
    alto=3.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    origen=(-3.0, -1.5, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)
habitacion2 = A.crear_habitacion(
    nombre="Habitacion_2",
    ancho=5.0,
    fondo=4.0,
    alto=3.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    origen=(3.0, -1.5, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)
hab_bano = A.crear_habitacion(
    nombre="Bano",
    ancho=3.0,
    fondo=2.5,
    alto=3.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    origen=(0, 4.0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Porcelanato",
    material_techo="Yeso"
)
hab_cocina = A.crear_habitacion(
    nombre="Cocina",
    ancho=4.0,
    fondo=3.0,
    alto=3.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    origen=(0, -3.0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Porcelanato",
    material_techo="Yeso"
)
hab_sala = A.crear_habitacion(
    nombre="Sala_Comedor",
    ancho=7.0,
    fondo=4.0,
    alto=3.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    origen=(-2.0, 0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)

# Añadir mobiliario
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.5,
    fondo=0.9,
    alto_asiento=0.45,
    alto_respaldo=0.85,
    origen=(0, 0, 0),
    material="Tela_Beige"
)

# Iluminación y cámara
A.agregar_luz("Luz_Solar", tipo="SUN", ubicacion=(5, -5, 10), energia=2.5)
A.crear_camara("Camara_Frontal", ubicacion=(0, -8, 5), rotacion=(80, 0, 0))