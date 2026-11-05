import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas tipo torre
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioApartamentos",
    pisos=4,
    ancho=15.0,
    fondo=20.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=False,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Crear balcones en voladizo
for i in range(4):
    for j in range(15):
        x = j * (15.0 / 16)
        z = i * 3.0 + 0.9 # Altura de losa + 0.9m de voladizo
        A.crear_losa_rectangular(f"Balcon_{i}_{j}", ancho=0.9, fondo=2.8, espesor=0.2, origen=(x-0.45, -1.4, z), material="Concreto_Piso")
        A.crear_losa_rectangular(f"Baranda_{i}_{j}", ancho=0.9, fondo=0.15, espesor=0.05, origen=(x-0.45, -1.45, z+0.9), material="Vidrio")

# Jardineras perimetrales
for i in range(4):
    for j in [0, 15]:
        x = j * (15.0 / 16)
        A.crear_losa_rectangular(f"Jardinera_{i}_{j}", ancho=0.9, fondo=2.8, espesor=0.4, origen=(x-0.45, -1.4, 3.0), material="Hormigon")

# Vegetacion
for i in range(4):
    for j in range(15):
        x = j * (15.0 / 16)
        A.crear_planta_simple(f"Planta_{i}_{j}", radio=0.2, altura=0.5, origen=(x-0.2, -1.4, 3.0))
        A.crear_arbol_simple(f"Arbol_{i}_{j}", radio_copa=1.2, altura_copa=2.5, altura_tronco=1.5, origen=(x-0.6, -1.4, 3.0))