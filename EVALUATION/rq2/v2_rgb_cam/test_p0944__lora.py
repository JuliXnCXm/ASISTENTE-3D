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

# Añadir mobiliario
mesa = A.crear_mesa(
    nombre="Mesa_Comedor",
    ancho=1.8,
    fondo=0.9,
    alto=0.75,
    origen=(2.5, 1.5, 0),
    material_tablero="Madera_Roble"
)
for i in range(6):
    silla = A.crear_silla(f"Silla_{i+1}", origen=(2.5 + i*0.3, 0.8, 0), material="Cuero")
    silla.rotation_euler[2] = 3.14159 # 180 grados

# Añadir iluminación ambiental
A.agregar_luz("Luz_Techo", tipo="AREA", ubicacion=(3, 2, 2.7), energia=200, color=(1, 0.9, 0.8))

# Añadir una ventana grande en la pared del fondo
A.crear_ventana(
    nombre="Ventana_Fondo",
    ancho=2.5,
    alto=1.2,
    prof_marco=0.15,
    origen=(1.75, 4.0, 1.0),
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)