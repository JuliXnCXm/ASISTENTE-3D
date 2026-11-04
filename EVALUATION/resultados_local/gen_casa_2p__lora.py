import blender_arch as A

A.limpiar_escena()

alto_piso = 2.8
grosor_muro = 0.2

casa = A.crear_casa_n_pisos(
    nombre="CasaFamiliar",
    pisos=2,
    ancho=8.0,
    fondo=10.0,
    alto_piso=alto_piso,
    grosor_muro=grosor_muro,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

A.crear_puerta(
    nombre="PuertaPrincipal",
    ancho=1.2,
    alto=2.2,
    prof_marco=grosor_muro,
    origen=(grosor_muro + 0.6, grosor_muro, 0),
    material_panel="Madera_Roble",
    material_marco="Marco_Blanco"
)

A.crear_ventana(
    nombre="VentanaFrontal1",
    ancho=1.5,
    alto=1.2,
    prof_marco=grosor_muro,
    origen=(3.0, grosor_muro, 1.0),
    material_vidrio="Vidrio",
    material_marco="Marco_Blanco"
)

A.crear_ventana(
    nombre="VentanaFrontal2",
    ancho=1.5,
    alto=1.2,
    prof_marco=grosor_muro,
    origen=(6.0, grosor_muro, 1.0),
    material_vidrio="Vidrio",
    material_marco="Marco_Blanco"
)