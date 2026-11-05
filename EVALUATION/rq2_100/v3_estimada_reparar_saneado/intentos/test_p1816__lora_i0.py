import blender_arch as A
A.limpiar_escena()

# Crear la estructura de la cocina
ancho_cocina = 5.0
fondo_cocina = 4.5
alto_muro = 2.8

A.crear_habitacion(
    nombre="Cocina",
    ancho=ancho_cocina,
    fondo=fondo_cocina,
    alto=alto_muro,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Porcelanato"
)

# Crear la isla central
ancho_isla = 1.8
fondo_isla = 0.9
alto_isla = 0.9

pos_isla_x = ancho_cocina / 2
pos_isla_y = fondo_cocina - fondo_isla / 2
A.crear_mesa(
    nombre="Isla_Cocina",
    ancho=ancho_isla,
    fondo=fondo_isla,
    alto=alto_isla,
    origen=(pos_isla_x, pos_isla_y, 0),
    material_tablero="Madera_Roble"
)

# Encimeras perimetrales
A.crear_mesa(
    nombre="Encimera_Izquierda",
    ancho=ancho_cocina,
    fondo=0.6,
    alto=0.9,
    origen=(0, 0.3, 0),
    material_tablero="Porcelanato"
)
A.crear_mesa(
    nombre="Encimera_Derecha",
    ancho=ancho_cocina,
    fondo=0.6,
    alto=0.9,
    origen=(0, fondo_cocina - 0.3, 0),
    material_tablero="Porcelanato"
)
A.crear_mesa(
    nombre="Encimera_Fondo",
    ancho=fondo_cocina,
    fondo=0.6,
    alto=0.9,
    origen=(ancho_cocina - 0.3, fondo_cocina / 2, 0),
    material_tablero="Porcelanato"
)

# Fregadero y fosa
ancho_fregadero = 0.6
fondo_fregadero = 0.4
fosa_ancho = 0.5
fosa_fondo = 0.4

pos_fregadero_x = ancho_cocina - fosa_ancho / 2
pos_fregadero_y = fondo_cocina - fosa_fondo / 2
A.crear_losa_rectangular(
    nombre="Fregadero",
    ancho=fosa_ancho,
    fondo=fosa_fondo,
    espesor=0.1,
    origen=(pos_fregadero_x, pos_fregadero_y, 0),
    material="Acero_Inox"
)
A.crear_losa_rectangular(
    nombre="Fosa",
    ancho=fosa_ancho,
    fondo=fosa_fondo,
    espesor=-0.1,
    origen=(pos_fregadero_x, pos_fregadero_y, 0),
    material="Porcelanato"
)

# Luces colgantes
A.agregar_luz(
    nombre="Luz_Isla_1",
    tipo="SPOT",
    ubicacion=(pos_isla_x, pos_isla_y + 0.7, alto_muro + 2.5),
    energia=500
)
A.agregar_luz(
    nombre="Luz_Isla_2",
    tipo="SPOT",
    ubicacion=(pos_isla_x, pos_isla_y - 0.7, alto_muro + 2.5),
    energia=500
)