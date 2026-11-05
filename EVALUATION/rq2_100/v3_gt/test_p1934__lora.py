import blender_arch as A

A.limpiar_escena()

# Crear la habitación base
hab = A.crear_habitacion(
    nombre="Dormitorio",
    ancho=3.0,
    fondo=3.5,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar la cama centrada en la pared del fondo
cama = A.crear_cama(
    nombre="Cama_Doble",
    ancho=1.6,
    largo=2.0,
    origen=(1.5, 3.5 - 0.1 - 2.0, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)

# Colocar mesitas de noche a ambos lados de la cama
mesita_izq = A.crear_mesa(
    nombre="Mesita_Izquierda",
    ancho=0.4, 
    fondo=0.4, 
    alto=0.6, 
    origen=(1.5 - 0.4/2 - 0.1, 1.0, 0), 
    material_tablero="Madera_Roble"
)
mesita_der = A.crear_mesa(
    nombre="Mesita_Derecha",
    ancho=0.4, 
    fondo=0.4, 
    alto=0.6, 
    origen=(1.5 + 0.4/2 + 0.1, 1.0, 0), 
    material_tablero="Madera_Roble"
)

# Colocar la lámpara de pie en la mesita derecha
lampara = A.crear_lampara_pie(
    nombre="Lampara_Noche",
    altura_total=1.8,
    altura_poste=0.9,
    origen=(1.5 + 0.4/2 + 0.1, 1.0, 0),
    material_parasol="Tela_Beige",
    material_base="Metal_Negro"
)