import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
hab = A.crear_habitacion(
    nombre="Oficina",
    ancho=4.0,
    fondo=3.0,
    alto=2.8,
    grosor_muro=0.15,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar mobiliario en L
A.crear_mesa(
    nombre="Escritorio_L",
    ancho=1.8,
    fondo=0.9,
    alto=0.75,
    origen=(1.6, 1.5, 0),
    material_tablero="Madera_Roble"
)
A.crear_silla(
    nombre="Silla_Oficina",
    origen=(1.6, 0.6, 0),
    material="Cuero"
)

# Estantería modular en la pared trasera
pos_estanteria = (2.0, 0.15, 0) # Centrada en X, pegada al muro
for i in range(4):
    A.crear_caja(
        nombre=f"Caja_Estanteria_{i}",
        ancho=0.3,
        fondo=0.3,
        alto=0.8,
        origen=pos_estanteria,
        rotacion_z=i * 90,
        material="MDF_Blanco"
    )
    pos_estanteria = (pos_estanteria[0], pos_estanteria[1] + 0.6, pos_estanteria[2])