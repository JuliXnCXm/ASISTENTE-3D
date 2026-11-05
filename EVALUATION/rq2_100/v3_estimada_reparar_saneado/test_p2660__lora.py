import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
hab = A.crear_habitacion(
    nombre="Salon",
    ancho=5.0,
    fondo=4.0,
    alto=2.8,
    grosor_muro=0.15,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet",
    material_techo="Yeso"
)

# Colocar mobiliario dentro de la habitación
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.2,
    origen=(1.4, 0.15, 0),
    material="Tela_Beige"
)

mesa = A.crear_mesa(
    nombre="Mesa_Centro",
    ancho=1.2,
    fondo=0.6,
    alto=0.45,
    origen=(2.4, 1.7, 0),
    material_tablero="Madera_Roble"
)