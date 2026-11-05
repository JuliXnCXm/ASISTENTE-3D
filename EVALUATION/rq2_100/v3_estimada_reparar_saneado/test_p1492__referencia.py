import blender_arch as A

A.limpiar_escena()

ancho_pergola = 4.0
fondo_pergola = 3.0
alto_pergola = 2.5
dim_columna = 0.2

# Coordenadas de las columnas
x_pos = (ancho_pergola - dim_columna) / 2
y_pos = (fondo_pergola - dim_columna) / 2
origenes = [
    (x_pos, y_pos, 0),
    (-x_pos, y_pos, 0),
    (x_pos, -y_pos, 0),
    (-x_pos, -y_pos, 0)
]

# Crear columnas
for i, origen in enumerate(origenes):
    A.crear_columna(
        nombre=f"Columna_Pergola_{i+1}",
        seccion="rect",
        ancho=dim_columna,
        fondo=dim_columna,
        alto=alto_pergola,
        origen=origen,
        material="Madera_Roble"
    )

# Crear techo (losa delgada)
A.crear_losa_rectangular(
    nombre="Techo_Pergola",
    ancho=ancho_pergola,
    fondo=fondo_pergola,
    espesor=0.15,
    origen=(0, 0, alto_pergola),
    material="Madera_Roble"
)