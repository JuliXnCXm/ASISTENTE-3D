import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
hab = A.crear_habitacion(
    nombre="OficinaCasa",
    ancho=3.5,
    fondo=4.0,
    alto=2.8,
    grosor_muro=0.15,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Añadir mobiliario
A.crear_silla(nombre="Silla_Oficina", origen=(1.5, 2.5, 0), material="Cuero")
A.crear_mesa(nombre="Escritorio", ancho=1.4, fondo=0.7, alto=0.75, origen=(0.8, 1.6, 0), material_tablero="Madera_Roble")

# Crear y posicionar la librería paramétrica
def crear_estanteria_parametrica(nombre, origen, ancho_total, alto_total, fondo, num_estantes):
    for i in range(num_estantes):
        altura = (alto_total / num_estantes) * i
        A.crear_estanteria(
            nombre=f"{nombre}_{i}",
            ancho=ancho_total,
            alto=alto_total,
            fondo=fondo,
            num_estantes=1,
            origen=(origen[0], origen[1], altura),
            material="MDF_Blanco"
        )

crear_estanteria_parametrica("Libreria", origen=(0.2, 0.2, 0), ancho_total=2.8, alto_total=2.2, fondo=0.3, num_estantes=10)