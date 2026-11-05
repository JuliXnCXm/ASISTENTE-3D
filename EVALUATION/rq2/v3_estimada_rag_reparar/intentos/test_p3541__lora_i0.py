import blender_arch as A

A.limpiar_escena()

# Edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioAzotea",
    pisos=4,
    ancho=12.0,
    fondo=15.0,
    alto_piso=2.8,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_techo_plano=True,
    con_columnas=True,
    seccion_columna="rect",
    dim_columna=(0.4, 0.4),
    modulo_columna_x=4.0,
    modulo_columna_y=5.0,
    origen=(-6, -7.5, 3.0)
)

# Suelo de terraza
A.crear_piso("SueloTerraza", ancho=12.0, fondo=15.0, espesor=0.1, origen=(-6, -7.5, 4.0), material="Madera")

# Pérgola
A.crear_techo_plano("Pergola", ancho=10.0, fondo=8.0, espesor=2.5, origen=(-5, -6, 4.0), material="Acero_Inox")

# Jardineras
for i in [-5, 5]:
    for j in [-6, 6]:
        A.crear_losa_rectangular(f"Jardinera_{i}_{j}", ancho=2.0, fondo=2.0, espesor=0.3, origen=(i-1, j-1, 4.0), material="Hormigon")
        A.crear_arbol_simple(f"Arbol_{i}_{j}", radio_copa=0.8, altura_copa=2.0, altura_tronco=1.2, origen=(i-1.1, j-1.1, 4.0))

# Mobiliario exterior
A.crear_sofa("Sofa_Azotea", ancho=2.5, fondo=0.9, origen=(-3, -5, 4.0), material="Tela_Beige")
A.crear_mesa("Mesa_Azotea", ancho=1.5, fondo=0.7, alto=0.45, origen=(-2, -4, 4.0), material_tablero="Madera_Roble")