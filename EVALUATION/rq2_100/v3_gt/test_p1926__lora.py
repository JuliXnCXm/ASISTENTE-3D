import blender_arch as A
A.limpiar_escena()

# Crear la estructura de la habitación
hab = A.crear_habitacion(
    nombre="Oficina",
    ancho=3.0,
    fondo=2.5,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar mobiliario
A.crear_mesa(
    nombre="Escritorio_Esquina",
    ancho=1.4,
    fondo=0.7,
    alto=0.75,
    origen=(0.8, 0.1, 0),
    material_tablero="Madera_Roble"
)
A.crear_silla(
    nombre="Silla_Oficina",
    origen=(1.5, 1.0, 0),
    material="Cuero"
)

# Librería paramétrica que se ajusta a la pared del fondo
ancho_libreria = 1.2
fondo_libreria = 0.3
alto_libreria = 2.2

# El origen de la librería se calcula para que quede pegada a la pared del fondo
origen_libreria_x = (3.0 - ancho_libreria) / 2
origen_libreria_y = 2.5 - fondo_libreria
origen_libreria_z = 0

libreria = A.crear_estanteria(
    nombre="Libreria_Oficina",
    ancho=ancho_libreria,
    alto=alto_libreria,
    fondo=fondo_libreria,
    num_estantes=5,
    origen=(origen_libreria_x, origen_libreria_y, origen_libreria_z),
    material="MDF_Blanco"
)