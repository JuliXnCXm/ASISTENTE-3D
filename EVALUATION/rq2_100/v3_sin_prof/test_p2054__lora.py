import blender_arch as A

A.limpiar_escena()

# Crear la base de la isla
A.crear_mesa(
    nombre="Isla_Cocina",
    ancho=2.0,
    fondo=1.0,
    alto=0.9,
    origen=(0, 0, 0),
    material_tablero="Cuarzo"
)

# Crear el fregadero integrado en la encimera
A.extruir_con_huecos(
    nombre="Fregadero_Impreso",
    contorno=[(-0.4, -0.5), (0.4, -0.5), (0.4, 0.5), (-0.4, 0.5)],
    agujeros=[[(-0.2, 0), (0.2, 0), (0.2, 0.1), (-0.2, 0.1)]],
    altura=-0.05,
    material="Acero_Inox"
).location = (0, 0, 0.9)

# Añadir iluminación
A.agregar_luz(
    nombre="Luz_Isla_1",
    tipo="SPOT",
    ubicacion=(-1.5, -2, 2.5),
    energia=800
)
A.agregar_luz(
    nombre="Luz_Isla_2",
    tipo="SPOT",
    ubicacion=(0, -2, 2.5),
    energia=800
)
A.agregar_luz(
    nombre="Luz_Isla_3",
    tipo="SPOT",
    ubicacion=(1.5, -2, 2.5),
    energia=800
)