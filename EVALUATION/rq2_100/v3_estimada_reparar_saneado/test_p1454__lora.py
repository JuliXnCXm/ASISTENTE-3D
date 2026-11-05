import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas corporativo
edificio = A.crear_edificio_n_pisos(
    nombre="TorreCorporativa",
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.8,
    ventana_alto=2.2,
    ventana_alfeizar=0.6,
    ventana_separacion=2.5,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Entrada principal en el primer piso
A.crear_puerta(
    nombre="PuertaEntrada",
    ancho=3.0,
    alto=2.2,
    prof_marco=0.2,
    origen=(7.5, 14.5, 0),
    material_panel="Vidrio_Templado",
    material_marco="Marco_Negro"
)