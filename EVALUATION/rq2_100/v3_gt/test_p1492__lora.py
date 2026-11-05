import blender_arch as A

A.limpiar_escena()

alto_pergola = 2.8
ancho_pergola = 4.0
fondo_pergola = 3.0
dim_columna = 0.2

# Crear las 4 columnas en las esquinas
posiciones_columnas = [
    (-ancho_pergola/2, -fondo_pergola/2, 0),
    (ancho_pergola/2, -fondo_pergola/2, 0),
    (-ancho_pergola/2, fondo_pergola/2, 0),
    (ancho_pergola/2, fondo_pergola/2, 0)
]

for i, pos in enumerate(posiciones_columnas):
    A.crear_columna(
        nombre=f"Columna_{i+1}",
        seccion="rect",
        ancho=dim_columna,
        fondo=dim_columna,
        alto=alto_pergola,
        origen=pos,
        material="Madera_Roble"
    )

# Crear el techo de la pérgola
ancho_techo = ancho_pergola + dim_columna
fondo_techo = fondo_pergola + dim_columna
A.crear_losa_rectangular(
    nombre="Techo_Pergola",
    ancho=ancho_techo,
    fondo=fondo_techo,
    espesor=0.15,
    origen=(0, 0, alto_pergola),
    material="Madera_Roble"
)