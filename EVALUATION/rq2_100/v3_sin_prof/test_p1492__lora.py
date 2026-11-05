import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho = 4.0
fondo = 3.0
alto = 2.5
dim_columna = 0.2
alto_viga = 0.15
num_vigas_larga = 8
num_vigas_corta = 6

# Crear columnas
pos_x = ancho / 2 - dim_columna / 2
pos_y = fondo / 2 - dim_columna / 2
for i in range(4):
    x = pos_x if i % 2 == 0 else -pos_x
    y = pos_y if i < 2 else -pos_y
    A.crear_columna(
        nombre=f"Columna_{i+1}",
        seccion="rect",
        ancho=dim_columna,
        fondo=dim_columna,
        alto=alto,
        origen=(x, y, 0),
        material="Madera_Roble"
    )

# Crear vigas largas (a lo largo de X)
for i in range(num_vigas_larga):
    x = 0
    y = pos_y + (dim_columna / 2) + (i * (fondo - dim_columna))
    A.crear_losa_rectangular(
        nombre=f"Viga_Larga_{i+1}",
        ancho=ancho,
        fondo=dim_columna,
        espesor=alto_viga,
        origen=(x, y, alto),
        material="Madera_Roble"
    )

# Crear vigas cortas (a lo largo de Y)
for i in range(num_vigas_corta):
    x = pos_x + (dim_columna / 2) + (i * (ancho - dim_columna))
    y = 0
    A.crear_losa_rectangular(
        nombre=f"Viga_Corta_{i+1}",
        ancho=dim_columna,
        fondo=fondo,
        espesor=alto_viga,
        origen=(x, y, alto),
        material="Madera_Roble"
    )

# Crear techo
A.crear_losa_rectangular(
    nombre="Techo_Pergola",
    ancho=ancho,
    fondo=fondo,
    espesor=0.15,
    origen=(0, 0, alto + alto_viga),
    material="Madera_Roble"
)