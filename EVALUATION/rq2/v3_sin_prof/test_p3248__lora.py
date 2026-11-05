import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas con fachada principal a la izquierda
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=4,
    ancho=15.0,
    fondo=12.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=False,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Crear balcones en voladizo
for i in range(4):
    x_pos = -7.5 + i * 3.0
    A.crear_losa_rectangular(f"Balcon_{i+1}", ancho=3.0, fondo=0.6, espesor=0.2, origen=(x_pos, -6.0, 2.9), material="Concreto_Piso")
    A.crear_losa_rectangular(f"Baranda_{i+1}", ancho=3.0, fondo=0.1, espesor=0.2, origen=(x_pos, -6.1, 2.9), material="Vidrio_Templado")

# Jardineras perimetrales en la terraza
for i in range(4):
    x_pos = -7.5 + i * 3.0
    A.crear_losa_rectangular(f"Jardinera_{i+1}", ancho=0.8, fondo=0.8, espesor=0.4, origen=(x_pos, -6.8, 4.1), material="Hormigon")

# Plantas de las jardineras
for i in range(4):
    x_pos = -7.5 + i * 3.0
    A.crear_arbol_simple(f"Planta_{i+1}", radio_copa=0.3, altura_copa=1.5, altura_tronco=0.8, origen=(x_pos, -6.8, 4.5))

# Iluminación y cámara
A.agregar_luz("LuzSol", tipo="SUN", ubicacion=(-10, -15, 15), energia=2.5)
A.crear_camara("CamaraFachada", ubicacion=(10, -15, 8), rotacion=(70, 0, 0))