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

# Colocar alfombra centrada
A.crear_alfombra(
    nombre="Alfombra_Sala",
    ancho=2.5,
    fondo=1.8,
    origen=(1.5, 1.6, 0),
    material="Tela_Beige"
)

# Colocar sofá contra la pared del fondo
sofa = A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.2,
    fondo=0.9,
    origen=(1.5, 3.0, 0),
    material="Tela_Gris"
)

# Colocar mueble de TV contra la pared frontal
mueble_tv = A.crear_mesa(
    nombre="Mueble_TV",
    ancho=1.8,
    fondo=0.4,
    alto=0.45,
    origen=(1.5, 0.2, 0),
    material_tablero="MDF_Blanco"
)

# Añadir panel de listones de madera vertical detrás del mueble
panel_listones = A.crear_panel_listones(
    nombre="Panel_Listones",
    ancho=1.8,
    alto=0.45,
    num_listones=12,
    origen=(1.5, 0.2, 0.45),
    material="Madera_Roble"
)