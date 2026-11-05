import blender_arch as A

A.limpiar_escena()

hab = A.crear_habitacion(
    nombre="Dormitorio",
    ancho=4.0,
    fondo=3.5,
    alto=2.7,
    grosor_muro=0.15,
    grosor_losa=0.2,
    con_suelo=True,
    con_techo=True,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)

cama = A.crear_cama(
    nombre="Cama_Doble",
    ancho=1.6,
    largo=2.0,
    alto_base=0.35,
    alto_cabecero=1.0,
    origen=(0.2, 0.2, 0),
    material_base="Madera_Roble",
    material_colchon="Textil_Blanco"
)

armario = A.crear_armario(
    nombre="Armario_Ropa",
    ancho=1.8,
    alto=2.4,
    fondo=0.6,
    num_puertas=2,
    origen=(1.1, 0.2, 0),
    material_cuerpo="MDF_Blanco",
    material_puerta="MDF_Blanco"
)

ventana = A.crear_ventana(
    nombre="Ventana_Dormitorio",
    ancho=1.2,
    alto=1.1,
    origen=(1.4, 0.2, 1.3),
    material_marco="Marco_Negro",
    material_vidrio="Vidrio"
)