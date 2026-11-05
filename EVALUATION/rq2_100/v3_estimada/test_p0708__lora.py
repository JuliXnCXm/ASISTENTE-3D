import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho_hab = 4.0
fondo_hab = 3.0
alto_hab = 2.8
grosor_muro = 0.15

# Crear la habitación
hab = A.crear_habitacion(
    nombre="Sala",
    ancho=ancho_hab,
    fondo=fondo_hab,
    alto=alto_hab,
    grosor_muro=grosor_muro,
    material_muro="Estuco",
    material_suelo="Ceramica_Piso"
)

# Abrir el vano para la puerta en el muro frontal
centro_vano_world = (ancho_hab / 2, grosor_muro / 2, alto_hab / 2)
A.abrir_vanos_batch_rectangulares(
    centros_world=[centro_vano_world],
    ancho=0.9,
    alto=2.1
)

# Crear y colocar la puerta en el vano
origen_puerta = (ancho_hab / 2, grosor_muro / 2, 0)
A.crear_puerta(
    nombre="Puerta_Acceso",
    ancho=0.9,
    alto=2.1,
    prof_marco=grosor_muro,
    origen=origen_puerta,
    material_panel="Madera_Roble",
    material_marco="Marco_Blanco"
)