import blender_arch as A
A.limpiar_escena()

# 1. Crear la base del deck
deck = A.crear_piso(
    nombre="Deck",
    ancho=6.0,
    fondo=4.0,
    espesor=0.15,
    material="Madera_Roble"
)

# 2. Crear las columnas de la pérgola
for i in [-1, 1]:
    for j in [-1, 1]:
        A.crear_columna(
            nombre=f"Columna_{i}_{j}",
            seccion="rect", ancho=0.2, fondo=0.2, alto=2.8,
            origen=(i*2.5, j*2.5, 0),
            material="Madera_Roble"
        )

# 3. Crear los travesaños de la pérgola
for i in range(4):
    pos_x = -1 + i * 1.5
    A.crear_losa_rectangular(
        nombre=f"Travesano_{i}",
        ancho=1.0,
        fondo=0.15,
        espesor=0.15,
        origen=(pos_x, -1.5, 2.8),
        material="Madera_Roble"
    )
    A.crear_losa_rectangular(
        nombre=f"Travesano_{i}_2",
        ancho=1.0,
        fondo=0.15,
        espesor=0.15,
        origen=(pos_x, 1.5, 2.8),
        material="Madera_Roble"
    )

# 4. Crear maceteros de hormigón
for i in [-1, 1]:
    for j in [-1, 1]:
        A.crear_conejo(
            nombre=f"Macetero_{i}_{j}",
            radio_base=1.2,
            altura_base=0.3,
            altura_copa=0.8,
            origen=(i*2.5, j*2.5, 0),
            material="Hormigon"
        )

# 5. Añadir vegetación
A.crear_arbol_simple(
    nombre="Arbol_1",
    radio_copa=1.0,
    altura_copa=2.0,
    altura_tronco=1.5,
    origen=(-2, -2, 0)
)
A.crear_arbol_simple(
    nombre="Arbol_2",
    radio_copa=0.8,
    altura_copa=1.5,
    altura_tronco=1.0,
    origen=(2, 2, 0)
)