import blender_arch as A

A.limpiar_escena()

# Dimensiones
ancho = 4.0
fondo = 3.0
alto = 2.8
dim_poste = 0.15
grosor_vigueta = 0.1
num_viguetas_x = 6
num_viguetas_y = 5

# Crear postes
posiciones_postes = [
    (-ancho/2, -fondo/2, alto/2),
    (ancho/2, -fondo/2, alto/2),
    (-ancho/2, fondo/2, alto/2),
    (ancho/2, fondo/2, alto/2)
]
for i, pos in enumerate(posiciones_postes):
    A.crear_columna(
        nombre=f"Poste_{i+1}",
        seccion="rect",
        ancho=dim_poste,
        fondo=dim_poste,
        alto=alto,
        origen=pos,
        material="Madera_Roble"
    )

# Crear viguetas principales (a lo largo de X)
for i in range(num_viguetas_x + 1):
    x_pos = -ancho/2 + i * (ancho / num_viguetas_x)
    A.crear_losa_rectangular(
        nombre=f"Vigueta_{i}",
        ancho=ancho,
        fondo=grosor_vigueta,
        espesor=0.15,
        origen=(x_pos, -fondo/2, alto),
        material="Madera_Roble"
    )

# Crear viguetas secundarias (a lo largo de Y)
for i in range(num_viguetas_y + 1):
    y_pos = -fondo/2 + i * (fondo / num_viguetas_y)
    A.crear_losa_rectangular(
        nombre=f"Vigueta_Secundaria_{i}",
        ancho=grosor_vigueta,
        fondo=fondo,
        espesor=0.15,
        origen=(-ancho/2, y_pos, alto + 0.15),
        material="Madera_Roble"
    )