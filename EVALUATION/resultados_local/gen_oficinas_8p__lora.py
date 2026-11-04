import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas corporativo
edificio = A.crear_edificio_n_pisos(
    nombre="TorreCorporativa",
    pisos=8,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.4,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Terreno circundante
A.crear_terreno_plano("TerrenoEdificio", ancho=40, fondo=30, espesor=0.15, origen=(0,0,-0.15), material="Cesped")

# Arbolado perimetral
for i in range(4):
    A.crear_arbol_simple(f"Arbol_Frente_{i}", radio_copa=2.0, altura_copa=4.0, altura_tronco=2.5, origen=(-10 + i*10, -8, 0))
    A.crear_arbol_simple(f"Arbol_Fondo_{i}", radio_copa=2.0, altura_copa=4.0, altura_tronco=2.5, origen=(-10 + i*10, 12, 0))