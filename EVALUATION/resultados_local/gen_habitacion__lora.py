import blender_arch as A

A.limpiar_escena()

ancho_hab = 4.0
fondo_hab = 3.5
alto_hab = 2.8
grosor_muro = 0.15

hab = A.crear_habitacion(
    nombre="Dormitorio",
    ancho=ancho_hab,
    fondo=fondo_hab,
    alto=alto_hab,
    grosor_muro=grosor_muro,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar cama contra la pared del fondo (Y+)
cama_x = (ancho_hab - 1.5) / 2
cama_y = fondo_hab - 1.0 - grosor_muro # 1.0m de largo, 0.1m de grosor
A.crear_cama(
    nombre="Cama_Doble",
    ancho=1.6,
    largo=2.0,
    origen=(cama_x, cama_y, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)

# Colocar armario contra la pared izquierda (X-)
armario_x = grosor_muro + 0.6
armario_y = fondo_hab / 2
A.crear_armario(
    nombre="Armario_Ropa",
    ancho=1.8,
    alto=2.4,
    fondo=0.6,
    num_puertas=2,
    origen=(armario_x, armario_y, 0),
    material_cuerpo="MDF_Blanco"
)

# Colocar ventana en la pared derecha (X+)
ventana_x = ancho_hab - grosor_muro - 1.0
ventana_y = fondo_hab / 2
A.crear_ventana(
    nombre="Ventana_Dormitorio",
    ancho=1.2,
    alto=1.1,
    prof_marco=grosor_muro,
    origen=(ventana_x, ventana_y, 0),
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)