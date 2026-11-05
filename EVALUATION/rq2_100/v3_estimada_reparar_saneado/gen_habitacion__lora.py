import blender_arch as A

A.limpiar_escena()

# Crear la habitación base
habitacion = A.crear_habitacion(
    nombre="Dormitorio",
    ancho=4.0,
    fondo=3.5,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar la cama centrada contra la pared del fondo (Y+)
A.crear_cama(
    nombre="Cama_Doble",
    ancho=1.6,
    largo=2.0,
    origen=(2.0, 3.5 - 2.0 - 0.1, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)

# Colocar un armario contra la pared izquierda (X-)
A.crear_armario(
    nombre="Armario",
    ancho=1.8,
    alto=2.4,
    fondo=0.6,
    origen=(0.1, 1.0, 0),
    material_cuerpo="MDF_Blanco"
)

# Colocar una ventana en la pared derecha (X+)
A.crear_ventana(
    nombre="Ventana_Dormitorio",
    ancho=1.5,
    alto=1.2,
    prof_marco=0.15,
    origen=(4.0 - 1.5, 1.5, 1.1),
    material_marco="Marco_Negro",
    material_vidrio="Vidrio"
)