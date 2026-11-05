import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas tipo torre
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=4,
    ancho=15.0,
    fondo=12.0,
    alto_piso=3.2,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=False,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_losa_terrazas="Concreto_Piso"
)

# Crear balcones en voladizo
for i in range(4):
    # Puerta de acceso
    A.crear_puerta(f"BalconPuerta_{i+1}", ancho=1.5, alto=2.2, prof_marco=0.2, origen=(7.5, 6 + i*3, 0), material_panel="Vidrio_Templado", material_marco="Marco_Negro")
    
    # Barandilla de vidrio
    for j in [-1, 0, 1]:
        A.crear_baranda_lineal(f"BalconBaranda_{i+1}_{j}", largo=1.8, origen=(7.5 + 0.2 + 0.9, 6 + i*3 + j*1.5, 2.2), material="Vidrio_Templado")

# Jardineras perimetrales en la terraza
for i in [-1, 0, 1]:
    A.crear_losa_rectangular(f"Jardinera_{i}", ancho=15.0, fondo=0.6, espesor=0.3, origen=(7.5, 6 + 3.0 + i*1.5, 12.8), material="Hormigon")
    A.crear_borda_planta(f"BordeJardinera_{i}", largo=15.0, alto=0.6, origen=(7.5 - 0.3, 6 + 3.0 + i*1.5, 13.1), material="Concreto_Piso")

# Arbolado perimetral
for i in range(8):
    A.crear_arbol_simple(f"Arbol_{i}", radio_copa=2.0, altura_copa=4.0, altura_tronco=2.5, origen=(-10 + i*2.5, -10, 0))