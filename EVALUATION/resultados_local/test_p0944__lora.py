import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
habitacion = A.crear_habitacion(
    nombre="Comedor",
    ancho=6.0,
    fondo=4.0,
    alto=2.8,
    grosor_muro=0.15,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar la mesa en el centro, contra la pared del fondo
mesa = A.crear_mesa(
    nombre="Mesa_Comedor",
    ancho=1.8,
    fondo=0.9,
    alto=0.76,
    origen=(3.0, 2.0 - 0.9/2, 0),
    material_tablero="Madera_Nogal"
)

# Colocar las sillas alrededor de la mesa
posiciones_sillas = [
    (2.2, 1.2, 0), (4.2, 1.2, 0), # Lado izquierdo
    (2.2, 2.8, 0), (4.2, 2.8, 0), # Lado derecho
    (3.0, 0.4, 0), (3.0, 3.6, 0)  # Cabeceras
]

for i, pos in enumerate(posiciones_sillas):
    silla = A.crear_silla(nombre=f"Silla_{i+1}", origen=pos, material="Madera_Nogal")

# Añadir iluminación ambiental
A.agregar_luz(
    nombre="Luz_Techo",
    tipo="AREA",
    ubicacion=(3.0, 2.0, 2.7),
    energia=250,
    color=(1.0, 0.9, 0.8)
)

# Añadir una ventana en la pared del fondo
A.crear_ventana(
    nombre="Ventana_Comedor",
    ancho=2.0,
    alto=1.2,
    prof_marco=0.15,
    origen=(2.0, 0, 0),
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)