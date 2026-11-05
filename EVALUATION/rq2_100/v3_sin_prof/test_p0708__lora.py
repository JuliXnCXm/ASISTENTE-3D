import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho_hab = 4.0
fondo_hab = 3.0
alto_hab = 2.8
grosor_muro = 0.15

# Crear la habitación
hab = A.crear_habitacion(
    nombre="Dormitorio",
    ancho=ancho_hab,
    fondo=fondo_hab,
    alto=alto_hab,
    grosor_muro=grosor_muro,
    material_muro="Estuco",
    material_suelo="Ceramica_Piso"
)

# Abrir hueco para la puerta en el muro frontal
muro_frontal = hab.children[0]
A.abrir_vanos_batch_rectangulares(muro_frontal, centros_world=[(0, -grosor_muro/2, 1.0)], ancho=0.9, alto=2.1)

# Crear y colocar la puerta en el hueco
origen_puerta = (0, -grosor_muro/2, 0)
A.crear_puerta(
    nombre="Puerta_Acceso",
    ancho=0.9,
    alto=2.1,
    prof_marco=grosor_muro,
    origen=origen_puerta,
    material_panel="Madera_Roble",
    material_marco="Marco_Blanco"
)