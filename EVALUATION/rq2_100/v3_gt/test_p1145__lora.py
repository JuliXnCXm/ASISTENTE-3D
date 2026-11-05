import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
hab = A.crear_habitacion(
    nombre="Estudio",
    ancho=6.0,
    fondo=5.0,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Mobiliario de descanso
A.crear_cama(
    nombre="Cama_Estudio",
    ancho=1.4,
    largo=2.0,
    origen=(1.3, 0.2, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)
A.crear_armario(
    nombre="Armario_Estudio",
    ancho=1.8,
    alto=2.4,
    fondo=0.6,
    origen=(0.2, 0.2, 0),
    material_cuerpo="MDF_Blanco"
)

# Mobiliario de trabajo
A.crear_mesa(
    nombre="Mesa_Trabajo",
    ancho=1.2,
    fondo=0.7,
    alto=0.75,
    origen=(2.5, 2.0, 0),
    material_tablero="Madera"
)
A.crear_silla(nombre="Silla_1", origen=(2.5, 1.5, 0), material="Madera")
A.crear_silla(nombre="Silla_2", origen=(2.5, 2.5, 0), material="Madera")

# Mobiliario de cocina
A.crear_encimera_lineal(
    nombre="Encimera_Cocina_1",
    largo=2.0,
    origen=(5.0, 0.2, 0),
    material="Porcelanato"
)
A.crear_encimera_lineal(
    nombre="Encimera_Cocina_2",
    largo=1.5,
    origen=(5.0, 1.5, 0),
    material="Porcelanato"
)