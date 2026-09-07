import blender_arch as A

A.limpiar_escena()

# Definir dimensiones
ancho_hab = 4.0
fondo_hab = 3.5
alto_hab = 2.8
grosor_muro = 0.15
grosor_suelo = 0.2

# Crear la habitación
A.crear_habitacion(
    nombre="Dormitorio",
    ancho=ancho_hab,
    fondo=fondo_hab,
    alto=alto_hab,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_suelo,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Crear y posicionar la cama dentro de la habitación
largo_cama = 2.0
origen_cama_x = ancho_hab / 2
origen_cama_y = fondo_hab - grosor_muro - (largo_cama / 2)
origen_cama_z = grosor_suelo

A.crear_cama(
    nombre="Cama_Doble",
    ancho=1.6,
    largo=largo_cama,
    alto_cabecero=1.1,
    origen=(origen_cama_x, origen_cama_y, origen_cama_z),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)