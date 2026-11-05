import blender_arch as A

A.limpiar_escena()

# Casa tipo Villa con patio
casa = A.crear_casa_n_pisos(
    nombre="CasaFamiliar",
    pisos=2,
    ancho=8.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    origen=(0, 0, 0),
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Puerta en el centro de la fachada frontal (Y=0)
A.crear_puerta(
    nombre="PuertaPrincipal",
    ancho=1.1,
    alto=2.1,
    prof_marco=0.2,
    origen=(3.45, -0.1, 0),
    material_panel="Madera_Roble",
    material_marco="Marco_Negro"
)

# Ventanas en las 3/4 superiores de la fachada frontal
A.crear_ventana(
    nombre="VentanaDerecha",
    ancho=1.5,
    alto=1.2,
    prof_marco=0.2,
    origen=(6.7, -0.1, 1.5),
    material_vidrio="Vidrio",
    material_marco="Marco_Negro"
)

A.crear_ventana(
    nombre="VentanaIzquierda",
    ancho=1.5,
    alto=1.2,
    prof_marco=0.2,
    origen=(1.3, -0.1, 1.5),
    material_vidrio="Vidrio",
    material_marco="Marco_Negro"
)