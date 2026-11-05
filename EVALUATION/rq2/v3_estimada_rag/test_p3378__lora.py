import blender_arch as A

A.limpiar_escena()

# --- Parámetros de la casa ---
ancho_total = 10.0
fondo_total = 8.0
alto_piso = 2.8
grosor_muro = 0.2
grosor_losa = 0.2
alto_cumbrera = 1.5
voladizo = 0.4
num_pisos = 2

# --- Crear la casa base ---
casa = A.crear_casa_n_pisos(
    nombre="ApartamentoDuplex",
    pisos=num_pisos,
    ancho=ancho_total,
    fondo=fondo_total,
    alto_piso=alto_piso,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    con_tejado=True,
    altura_cumbrera=alto_cumbrera,
    voladizo=voladizo,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# --- Crear la escalera ---
huella = 0.28
contrahuella = 0.175
ancho_escalera = 1.1
num_peldanos = 16
grosor_peldano = 0.03
origen_escalera = (ancho_total/2, fondo_total - 1.5, 0) # Centrada en X, contrafachada en Y, sobre la losa inferior

A.crear_escalera_recta(
    nombre="Escalera_Principal",
    huella=huella,
    contrahuella=contrahuella,
    ancho=ancho_escalera,
    num_peldanos=num_peldanos,
    grosor_peldano=grosor_peldano,
    con_contrahuellas=True,
    con_zancas=True,
    espesor_zanca=0.15,
    origen=origen_escalera,
    material="Hormigon"
)

# --- Mobiliario planta baja (piso 1) ---
# Sala de estar
A.crear_habitacion(
    nombre="Sala_Estar",
    ancho=5.0,
    fondo=4.0,
    alto=2.8,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)
# Comedor
A.crear_habitacion(
    nombre="Comedor",
    ancho=4.0,
    fondo=3.0,
    alto=2.8,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    origen=(ancho_total - 4.0, 0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Porcelanato",
    material_techo="Yeso"
)
# Cocina
A.crear_habitacion(
    nombre="Cocina",
    ancho=3.0,
    fondo=2.5,
    alto=2.8,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    origen=(ancho_total - 3.0, 2.5, 0),
    material_muro="Muro_Pintura",
    material_suelo="Porcelanato",
    material_techo="Yeso"
)
# Aseo
A.crear_habitacion(
    nombre="Aseo_Bajo",
    ancho=2.0,
    fondo=1.5,
    alto=2.8,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    origen=(ancho_total - 2.0, 1.5, 0),
    material_muro="Muro_Pintura",
    material_suelo="Ceramica_Piso",
    material_techo="Yeso"
)

# --- Mobiliario planta alta (piso 2) ---
# Dormitorio Principal
A.crear_habitacion(
    nombre="Dormitorio_Principal",
    ancho=4.0,
    fondo=4.0,
    alto=2.8,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    origen=(0, fondo_total - 4.0, alto_piso),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)
# Dormitorio Secundario
A.crear_habitacion(
    nombre="Dormitorio_Secundario",
    ancho=3.0,
    fondo=3.0,
    alto=2.8,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    origen=(ancho_total - 3.0, fondo_total - 3.0, alto_piso),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)
# Baño Compartido
A.crear_habitacion(
    nombre="Bano_Compartido",
    ancho=2.0,
    fondo=1.5,
    alto=2.8,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    origen=(ancho_total - 2.0, 1.5, alto_piso),
    material_muro="Muro_Pintura",
    material_suelo="Ceramica_Piso",
    material_techo="Yeso"
)