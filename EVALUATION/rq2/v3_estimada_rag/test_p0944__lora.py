import blender_arch as A

A.limpiar_escena()

# Crear la habitación base
hab = A.crear_habitacion(
    nombre="Comedor",
    ancho=6.0,
    fondo=4.0,
    alto=2.8,
    grosor_muro=0.15,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura",
    material_suelo="Parquet"
)

# Colocar la mesa en el centro de la habitación
mesa = A.crear_mesa(
    nombre="MesaComedor",
    ancho=1.8,
    fondo=0.9,
    alto=0.75,
    grosor_tablero=0.04,
    origen=(0, 0, 0),
    material_tablero="Madera_Roble",
    material_patas="Acero_Inox"
)

# Colocar sillas alrededor de la mesa
for i in range(6):
    angulo = i * (360 / 6)
    x_pos = 0.9 + 0.45 * (i % 2) - 0.2
    y_pos = 0.45 * (i // 2)
    silla = A.crear_silla(
        nombre=f"Silla_{i+1}",
        ancho=0.45,
        fondo=0.45,
        alto_asiento=0.45,
        alto_respaldo=0.9,
        origen=(x_pos, y_pos, 0),
        material="Madera_Roble"
    )

# Añadir una ventana grande en la pared del fondo
A.crear_ventana(
    nombre="VentanaComedor",
    ancho=2.5,
    alto=1.2,
    prof_marco=0.15,
    origen=(1.25, 4.0 - 0.15, 1.1),
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)

# Añadir iluminación ambiental
A.agregar_luz(
    nombre="LuzTecho",
    tipo="AREA",
    ubicacion=(3.0, 2.0, 2.7),
    energia=200,
    color=(1.0, 0.9, 0.8)
)