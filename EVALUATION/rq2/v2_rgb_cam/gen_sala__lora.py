import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
A.crear_habitacion(
    nombre="SalaDeEstar",
    ancho=6.0,
    fondo=5.0,
    alto=2.8,
    material_muro="Estuco",
    material_suelo="Parquet"
)

# Colocar mobiliario
A.crear_sofa(
    nombre="SofaPrincipal",
    ancho=2.4,
    origen=(1.8, 0.3, 0),
    material="Tela_Gris"
)
A.crear_mesa(
    nombre="MesaCentro",
    ancho=1.2,
    fondo=0.6,
    alto=0.45,
    origen=(2.4, 2.5, 0),
    material_tablero="Madera_Roble"
)
A.crear_silla(
    nombre="Silla1",
    origen=(0.9, 3.0, 0),
    material="Cuero"
)
A.crear_silla(
    nombre="Silla2",
    origen=(4.5, 3.0, 0),
    material="Cuero"
)

# Crear y posicionar una ventana grande
A.crear_ventana(
    nombre="VentanaSala",
    ancho=2.5,
    alto=1.5,
    prof_marco=0.2,
    origen=(1.75, 4.8, 0),
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)