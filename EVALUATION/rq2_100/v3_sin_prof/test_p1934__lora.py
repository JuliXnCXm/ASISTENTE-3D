import blender_arch as A

A.limpiar_escena()

# Crear la habitación base
hab = A.crear_habitacion(
    nombre="Dormitorio",
    ancho=3.0,
    fondo=4.0,
    alto=2.7,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Añadir mobiliario
A.crear_cama(
    nombre="Cama_Doble",
    ancho=1.6,
    largo=2.0,
    origen=(1.5, 2.0, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)
A.crear_mesa(
    nombre="Mesita_1",
    ancho=0.5,
    fondo=0.5,
    alto=0.6,
    origen=(0.9, 0.5, 0),
    material_tablero="Madera_Roble"
)
A.crear_mesa(
    nombre="Mesita_2",
    ancho=0.5,
    fondo=0.5,
    alto=0.6,
    origen=(2.1, 0.5, 0),
    material_tablero="Madera_Roble"
)

# Añadir iluminación
A.agregar_luz(
    nombre="Luz_Techo",
    tipo="AREA",
    ubicacion=(1.5, 2.0, 2.6),
    energia=200,
    color=(1.0, 0.9, 0.8)
)
A.agregar_luz(
    nombre="Luz_Pie_Lampara",
    tipo="SPOT",
    ubicacion=(1.5, 0.5, 1.8),
    energia=150,
    color=(1.0, 0.9, 0.8)
)