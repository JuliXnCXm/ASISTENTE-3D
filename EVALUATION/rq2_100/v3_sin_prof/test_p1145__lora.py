import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
hab = A.crear_habitacion(
    nombre="Estudio",
    ancho=6.0,
    fondo=5.0,
    alto=2.8,
    grosor_muro=0.15,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Zona de descanso
A.crear_cama(
    nombre="Cama_Estudio",
    ancho=1.4,
    largo=2.0,
    origen=(1.3, 0.15, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)
A.crear_armario(
    nombre="Armario_Estudio",
    ancho=1.8,
    alto=2.4,
    fondo=0.6,
    num_puertas=2,
    origen=(0.15, 0.6, 0),
    material_cuerpo="MDF_Blanco"
)

# Zona de trabajo / comedor
A.crear_mesa(
    nombre="Mesa_Estudio",
    ancho=1.2,
    fondo=0.7,
    alto=0.75,
    origen=(2.4, 2.5, 0),
    material_tablero="Madera"
)
A.crear_silla(nombre="Silla_1", origen=(2.4, 1.8, 0), material="Madera")
A.crear_silla(nombre="Silla_2", origen=(2.4, 3.2, 0), material="Madera")

# Zona de cocina
encimera1 = A.crear_mesa(
    nombre="Encimera_Cocina_1",
    ancho=1.5,
    fondo=0.6,
    alto=0.9,
    origen=(4.5, 0.15, 0),
    material_tablero="Porcelanato"
)
encimera2 = A.crear_mesa(
    nombre="Encimera_Cocina_2",
    ancho=1.5,
    fondo=0.6,
    alto=0.9,
    origen=(4.5, 4.4, 0),
    material_tablero="Porcelanato"
)