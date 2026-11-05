import blender_arch as A
A.limpiar_escena()

# Crear la estructura de la cocina
ancho_cocina = 5.0
fondo_cocina = 4.0
alto_muro = 2.7

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
pos_isla_y = fondo_cocina + fondo_isla / 2
pos_isla_z = alto_isla / 2

A.crear_mesa(
    nombre="Isla_Cocina",
    ancho=ancho_isla,
    fondo=fondo_isla,
    alto=alto_isla,
    origen=(pos_isla_x, pos_isla_y, pos_isla_z),
    material_tablero="Madera_Roble"
)

# Encimera de la isla
A.crear_losa_rectangular(
    nombre="Encimera_Isla",
    ancho=ancho_isla,
    fondo=fondo_isla,
    espesor=0.04,
    origen=(pos_isla_x, pos_isla_y, alto_isla),
    material="Concreto_Piso"
)

# Fregadero en la isla
A.crear_losa_rectangular(
    nombre="Fregadero_Isla",
    ancho=0.6,
    fondo=0.4,
    espesor=0.1,
    origen=(pos_isla_x, pos_isla_y - 0.2, alto_isla),
    material="Acero_Inox"
)

# Luces colgantes sobre la isla
num_luces = 3
for i in range(num_luces):
    pos_x = pos_isla_x - 0.5 + i * 0.5
    A.agregar_luz(
        nombre=f"Luz_Isla_{i+1}",
        tipo="SPOT",
        ubicacion=(pos_x, 1.5, 2.5),
        energia=500
    )
    A.agregar_luz(
        nombre=f"Luz_Isla_{i+1}_shadow",
        tipo="POINT_SHADOW",
        ubicacion=(pos_x, 1.5, 2.5),
        energia=500
    )