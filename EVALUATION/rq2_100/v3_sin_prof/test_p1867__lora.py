import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
hab = A.crear_habitacion(
    nombre="Oficina",
    ancho=4.0,
    fondo=3.5,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar mobiliario en la oficina
A.crear_mesa(
    nombre="Escritorio_L",
    ancho=1.8,
    fondo=0.9,
    alto=0.75,
    origen=(1.6, 1.5, 0),
    material_tablero="Madera_Roble"
)
A.crear_estanteria(
    nombre="Estanteria_Oficina",
    ancho=1.2,
    alto=2.2,
    fondo=0.3,
    num_estantes=5,
    origen=(0.8, 1.0, 0),
    material="Madera_Roble"
)
A.crear_silla(
    nombre="Silla_Oficina",
    origen=(1.6, 0.8, 0),
    material="Cuero"
)