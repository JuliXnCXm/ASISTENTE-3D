import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
hab = A.crear_habitacion(
    nombre="Sala_Estar",
    ancho=4.5,
    fondo=4.0,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar una alfombra centrada
A.crear_alfombra(
    nombre="Alfombra_Sala",
    ancho=3.0,
    fondo=2.0,
    origen=(1.25, 1.5, 0),
    material="Textil_Beige"
)

# Colocar un sofá contra la pared del fondo
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.2,
    fondo=0.9,
    origen=(1.15, 1.6, 0),
    material="Tela_Gris"
)

# Colocar un mueble de TV contra la pared frontal
mueble_tv = A.crear_mesa(
    nombre="Mueble_TV",
    ancho=1.8,
    fondo=0.4,
    alto=0.45,
    origen=(1.35, 0.2, 0),
    material_tablero="MDF_Blanco"
)

# Añadir un panel de listones de madera vertical detrás del mueble
panel_listones = A.crear_panel_listones(
    nombre="Panel_Listones",
    ancho=1.8,
    alto=0.45,
    num_listones=12,
    origen=(1.35, 0.2, 0.45),
    material="Madera_Roble"
)