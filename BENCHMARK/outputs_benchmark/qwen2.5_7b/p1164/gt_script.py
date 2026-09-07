import blender_arch as A

A.limpiar_escena()

ancho_hab, fondo_hab = 4.0, 5.0

# Crear la habitación sin techo para ver el interior
A.crear_habitacion(
    'Dormitorio',
    ancho=ancho_hab, 
    fondo=fondo_hab, 
    alto=2.8, 
    material_muro='Muro_Pintura', 
    material_suelo='Parquet', 
    con_techo=False
)

# Colocar la cama centrada en la pared del fondo
ancho_cama = 1.6
largo_cama = 2.0
A.crear_cama(
    'Cama_Principal',
    ancho=ancho_cama, 
    largo=largo_cama, 
    origen=((ancho_hab - ancho_cama) / 2, fondo_hab - largo_cama - 0.1, 0), 
    material_base='Madera', 
    material_colchon='Textil_Blanco'
)

# Colocar el armario en la esquina frontal izquierda
A.crear_armario(
    'Armario_Ropa',
    ancho=1.8, 
    fondo=0.6,
    origen=(0.1, 0.1, 0), 
    material_cuerpo='MDF_Blanco'
)