import blender_arch as A
A.limpiar_escena()

# 1. Crear la base de la terraza
A.crear_losa_rectangular(
    nombre="Cubierta_Azotea",
    ancho=12.0,
    fondo=10.0,
    espesor=0.2,
    origen=(0, 0, 0),
    material="Concreto_Piso"
)

# 2. Crear el deck de madera
A.crear_losa_rectangular(
    nombre="Deck_Madera",
    ancho=10.0,
    fondo=8.0,
    espesor=0.15,
    origen=(0, 0, 0.2),
    material="Madera_Roble"
)

# 3. Jardineras de obra en el perímetro
for i in range(4):
    x = -5 + i * 3
    A.crear_muro(
        nombre=f"Jardinera_{i}",
        largo=3.0,
        alto=0.8,
        grosor=0.15,
        origen=(x, -5, 0.2),
        material="Hormigon"
    )

# 4. Mobiliario exterior
A.crear_sofa(
    nombre="Sofa_Exterior",
    ancho=2.0,
    fondo=0.9,
    origen=(-2, 2, 0.2),
    material="Madera"
)
A.crear_mesa(
    nombre="Mesa_Exterior",
    ancho=1.2,
    fondo=0.7,
    alto=0.7,
    origen=(0, 0, 0.2),
    material_tablero="Madera"
)

# 5. Pérgola de metal
A.crear_techo_viga(
    nombre="Pergola_Viga_Principal",
    largo=4.0,
    alto=2.5,
    origen=(-4, -4, 0.2),
    material="Acero_Inox"
)
A.crear_techo_viga(
    nombre="Pergola_Viga_Secundaria",
    largo=4.0,
    alto=2.5,
    origen=(-4, 4, 0.2),
    material="Acero_Inox"
)