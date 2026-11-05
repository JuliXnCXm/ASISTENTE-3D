import blender_arch as A

A.limpiar_escena()

# Crear la base de la isla
isla_base = A.crear_mesa(
    nombre="Isla_Cocina",
    ancho=2.0,
    fondo=0.9,
    alto=0.9,
    origen=(0, 0, 0),
    material_tablero="MDF_Blanco"
)

# Crear la encimera de cuarzo personalizada
encimera = A.crear_losa_rectangular(
    nombre="Encimera_Isla",
    ancho=2.0,
    fondo=0.9,
    espesor=0.04,
    origen=(0, 0, 0.9),
    material="Cuarzo"
)

# Crear el fregadero integrado
fregadero = A.crear_losa_rectangular(
    nombre="Fregadero_Isla",
    ancho=0.6,
    fondo=0.45,
    espesor=0.15,
    origen=(-0.7, -0.25, 0.9),
    material="Acero_Inox"
)

# Añadir iluminación
A.agregar_luz(
    nombre="Luz_Isla_1",
    tipo="POINT",
    ubicacion=(0, 0, 3.0),
    energia=150
)
A.agregar_luz(
    nombre="Luz_Isla_2",
    tipo="POINT",
    ubicacion=(-1.2, 0.6, 3.0),
    energia=150
)
A.agregar_luz(
    nombre="Luz_Isla_3",
    tipo="POINT",
    ubicacion=(1.2, 0.6, 3.0),
    energia=150
)