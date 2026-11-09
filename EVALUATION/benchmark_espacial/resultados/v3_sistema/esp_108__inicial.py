import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho = 8.0
fondo = 10.0
alto_piso = 3.0
grosor_muro = 0.25
altura_cumbrera = 2.0
angulo_cumbrera = 10.0

# Crear el volumen base de la casa
volumen_casa = A.crear_habitacion(
    nombre="Casa_Principal",
    ancho=ancho,
    fondo=fondo,
    alto=alto_piso,
    grosor_muro=grosor_muro,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Crear el techo mono-pendiente
A.crear_techo_pendiente(
    nombre="Techo_Cumbrera",
    ancho=ancho,
    fondo=fondo,
    altura_cumbrera=altura_cumbrera,
    voladizo_x=0.5,
    voladizo_y=0.5,
    origen=(0, 0, alto_piso),
    material="Teja"
)