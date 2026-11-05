import blender_arch as A
A.limpiar_escena()

# Edificio de apartamentos con parámetros dinámicos
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Apartamentos",
    pisos=4,
    ancho=15.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_x=5.0,
    modulo_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=2.0,
    ventana_alfeizar=1.0,
    ventana_separacion=2.5,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Azotea ajardinada
A.crear_losa_rectangular("Azotea_Jardin", ancho=15.0, fondo=8.0, espesor=0.2, origen=(0, 0, 12.0), material="Concreto_Piso")
A.crear_terreno_plano("Jardin_Azotea", ancho=15.0, fondo=8.0, espesor=0.2, origen=(0, 0, 12.2), material="Cesped")

# Balcones con blender_arch
for p in range(4):
    for i in range(3):
        x_pos = i * 5.0 + 2.5 # Centrado en el módulo
        z_pos = p * 3.0 + 1.0 # Altura del primer vano
        A.crear_losa_rectangular(f"Balcon_{p}_{i}", ancho=2.5, fondo=1.2, espesor=0.2, origen=(x_pos, 0, z_pos), material="Hormigon")
        A.crear_baranda_lineal(f"Baranda_{p}_{i}", largo=2.5, origen=(x_pos, -0.1, z_pos + 1.2), material="Acero_Inox")
        A.crear_baranda_lineal(f"Baranda_Top_{p}_{i}", largo=2.5, origen=(x_pos, 0.1, z_pos + 1.2), material="Acero_Inox")