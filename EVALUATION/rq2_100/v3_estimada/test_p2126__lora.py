import blender_arch as A
A.limpiar_escena()

# 1. Crear la base del deck
deck = A.crear_piso(
    nombre="Deck",
    ancho=10.0,
    fondo=8.0,
    espesor=0.15,
    origen=(0, 0, 0),
    material="Madera_Roble"
)

# 2. Crear soportes de la pérgola
soportes = []
for i in [-4, 4]:
    for j in [-3, 3]:
        loc_x = i * 2.5
        loc_y = j * 2.5
        soporte = A.crear_columna(
            nombre=f"Poste_{i}_{j}",
            seccion="rect",
            ancho=0.2,
            fondo=0.2,
            alto=2.8,
            origen=(loc_x, loc_y, 0),
            material="Madera_Roble"
        )
        soportes.append(soporte)

# 3. Crear vigas principales y transversales
num_vigas_principales = 5
num_vigas_transversales = 7

for i in range(num_vigas_principales):
    x_pos = -4 + i * 2.5
    viga_principal = A.crear_losa_rectangular(
        nombre=f"VigaPrincipal_{i}",
        ancho=0.2,
        fondo=0.2,
        espesor=0.2,
        origen=(x_pos, -3, 2.8),
        material="Madera_Roble"
    )

for i in range(num_vigas_transversales):
    y_pos = -3 + i * 2.5
    viga_transversal = A.crear_losa_rectangular(
        nombre=f"VigaTransversal_{i}",
        ancho=10.0,
        fondo=0.2,
        espesor=0.2,
        origen=(-4, y_pos, 3.0),
        material="Madera_Roble"
    )

# 4. Crear maceteros de hormigón
macetero1 = A.crear_cono(
    nombre="Macetero.001",
    radio=1.2,
    altura=0.8,
    origen=(-3, 3, 0),
    material="Hormigon"
)
macetero2 = macetero1.copy()
macetero2.location.x = 3
macetero2.rotation_euler[2] = 1.5708 # 90 grados

# 5. Añadir vegetación
A.crear_arbol_simple(
    nombre="Arbol.001",
    radio_copa=1.0,
    altura_copa=2.0,
    altura_tronco=1.5,
    origen=(-2, -2, 0)
)
A.crear_arbol_simple(
    nombre="Arbol.002",
    radio_copa=1.0,
    altura_copa=2.0,
    altura_tronco=1.5,
    origen=(2, 2, 0)
)