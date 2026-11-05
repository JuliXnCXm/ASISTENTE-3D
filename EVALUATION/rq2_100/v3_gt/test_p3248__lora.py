import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas con fachada principal a la izquierda
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Apartamentos",
    pisos=4,
    ancho=15.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=False,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_tejado="Cobre"
)

# Crear balcones en voladizo
for i in range(4):
    x_pos = -7.5 + i * 3.0
    A.crear_losa_rectangular(f"Balcon_{i+1}", ancho=2.9, fondo=0.6, espesor=0.2, origen=(x_pos, -6.0, 1.2), material="Concreto_Piso")
    A.crear_baranda_lineal(f"Baranda_{i+1}", largo=2.9, origen=(x_pos, -6.0, 1.4), material="Vidrio_Templado")

# Jardineras perimetrales en la terraza
for i in range(4):
    x_pos = -7.5 + i * 3.0
    A.crear_losa_rectangular(f"Jardinera_{i+1}", ancho=3.2, fondo=0.5, espesor=0.3, origen=(x_pos, -6.0, 3.2), material="Hormigon")
    A.crear_borda("Borde_Jardinera", largo=3.2, origen=(x_pos, -6.0, 3.5), material="Concreto_Piso_Pintura_Negro")

# Vegetacion en las jardineras
for i in range(4):
    x_pos = -7.5 + i * 3.0
    A.crear_arbol_simple(f"Arbol_{i+1}", radio_copa=1.2, altura_copa=2.5, altura_tronco=1.8, origen=(x_pos, -6.0, 3.5))

# Iluminacion y camara
A.agregar_luz("Luz_Principal", tipo="SUN", ubicacion=(-10, -15, 15), energia=3.0)
A.crear_camara("Camara_Fachada", ubicacion=(10, -15, 8), rotacion=(70, 0, 0))