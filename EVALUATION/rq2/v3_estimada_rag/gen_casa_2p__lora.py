import blender_arch as A

A.limpiar_escena()

# Casa tipo con ventanas y puerta
A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_tejado=True,
    altura_cumbrera=1.5,
    voladizo=0.4,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Puerta en el centro de la fachada frontal
A.crear_puerta(
    nombre="Puerta_Principal",
    ancho=1.0,
    alto=2.1,
    prof_marco=0.2,
    origen=(4.5, -0.1, 0),
    material_panel="Madera_Roble",
    material_marco="Marco_Negro"
)

# Ventanas en la fachada frontal
A.crear_ventana(
    nombre="Ventana_Frontal_1",
    ancho=1.5,
    alto=1.2,
    prof_marco=0.2,
    origen=(2.0, -0.1, 1.0),
    material_vidrio="Vidrio",
    material_marco="Marco_Aluminio"
)
A.crear_ventana(
    nombre="Ventana_Frontal_2",
    ancho=1.5,
    alto=1.2,
    prof_marco=0.2,
    origen=(7.0, -0.1, 1.0),
    material_vidrio="Vidrio",
    material_marco="Marco_Aluminio"
)