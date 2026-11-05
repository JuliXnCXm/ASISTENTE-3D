import blender_arch as A

A.limpiar_escena()

# Crear la habitación base
hab = A.crear_habitacion(
    nombre="Dormitorio",
    ancho=4.0,
    fondo=5.0,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Añadir mobiliario
A.crear_cama(
    nombre="Cama_Doble",
    ancho=1.6,
    largo=2.0,
    origen=(1.2, 0.2, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)

# Muro bajo para vestidor
A.crear_muro(
    nombre="Muro_Vestidor",
    largo=2.0,
    alto=0.9,
    origen=(1.0, 4.0, 0),
    material="MDF_Blanco"
)

# Armarios empotrados
A.crear_armario(
    nombre="Armario_1",
    ancho=1.8,
    alto=2.4,
    fondo=0.6,
    origen=(1.1, 0.2, 0),
    material_cuerpo="MDF_Blanco"
)
A.crear_armario(
    nombre="Armario_2",
    ancho=1.8,
    alto=2.4,
    fondo=0.6,
    origen=(1.1, 4.4, 0),
    material_cuerpo="MDF_Blanco"
)