import blender_arch as A

A.limpiar_escena()

# Crear la habitación base
habitacion = A.crear_habitacion(
    nombre="Comedor",
    ancho=6.0,
    fondo=4.0,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Añadir mobiliario
mesa = A.crear_mesa(
    nombre="Mesa_Comedor",
    ancho=1.8,
    fondo=0.9,
    alto=0.75,
    origen=(2.0, 1.5, 0),
    material_tablero="Madera_Roble"
)
for i in range(6):
    silla = A.crear_silla(nombre=f"Silla_{i+1}", origen=(2.0 + i*0.3, 0.8, 0), material="Acero_Inox")

# Añadir ventana en la pared larga
ventana_ancho = 2.0
ventana_alto = 1.2
ventana_origen = (3.0, 0.2, 1.1)
A.crear_ventana(
    nombre="Ventana_Comedor",
    ancho=ventana_ancho,
    alto=ventana_alto,
    prof_marco=0.1,
    divisiones=(2, 1),
    origen=ventana_origen,
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)

# Añadir iluminación ambiental
A.agregar_luz(
    nombre="Luz_Techo",
    tipo="AREA",
    ubicacion=(3.0, 2.0, 2.7),
    energia=200,
    color=(1.0, 0.9, 0.8)
)