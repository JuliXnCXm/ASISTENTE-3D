import blender_arch as A

A.limpiar_escena()

hab = A.crear_habitacion(
    nombre="Sala_Estar",
    ancho=6.0,
    fondo=5.0,
    alto=2.8,
    grosor_muro=0.15,
    grosor_losa=0.2,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet",
    material_techo="Yeso"
)

sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.2,
    fondo=0.9,
    alto_asiento=0.45,
    alto_respaldo=0.85,
    origen=(1.4, 0.2, 0),
    material="Tela_Gris"
)

mesa = A.crear_mesa(
    nombre="Mesa_Centro",
    ancho=1.2,
    fondo=0.6,
    alto=0.45,
    origen=(2.4, 2.2, 0),
    material_tablero="Madera_Roble"
)

silla1 = A.crear_silla(
    nombre="Silla_1",
    ancho=0.45,
    fondo=0.45,
    alto_asiento=0.45,
    alto_respaldo=0.9,
    origen=(1.5, 3.5, 0),
    material="Madera"
)

silla2 = A.crear_silla(
    nombre="Silla_2",
    ancho=0.45,
    fondo=0.45,
    alto_asiento=0.45,
    alto_respaldo=0.9,
    origen=(4.5, 3.5, 0),
    material="Madera"
)