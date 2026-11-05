import blender_arch as A
A.limpiar_escena()

# Edificio de apartamentos con fachada modular
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioModular",
    pisos=4,
    ancho=15.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_x=5.0,
    modulo_y=8.0,
    origen=(0, 0, 0),
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio",
    material_columna="Hormigon_Visto"
)

# Balcones en los modulos exteriores
for p in range(4):
    for i in [-1, 0, 1]:
        x = -7.5 + i * 5.0
        A.crear_losa_rectangular(f"Balcon_{p+1}_{i}", ancho=2.5, fondo=1.2, espesor=0.2, origen=(x, 0, 2.8), material="Concreto_Piso")
        A.crear_baranda_lineal(f"Baranda_{p+1}_{i}", largo=2.5, origen=(x, -0.6, 2.8), material="Acero_Inox")

# Azotea ajardinada
A.crear_terreno_plano("Azotea", ancho=15.0, fondo=8.0, espesor=0.3, origen=(0, 0, 12.0), material="Cesped")