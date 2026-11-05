import blender_arch as A
A.limpiar_escena()

# Casa tipo Villa con parámetros personalizados
casa = A.crear_casa_n_pisos(
    nombre="CasaFamiliar",
    pisos=2,
    ancho=12.0, fondo=9.0, alto_piso=2.8,
    grosor_muro=0.2, grosor_losa=0.2,
    con_tejado=True, altura_cumbrera=2.0, voladizo=0.6,
    material_muro="Ladrillo", material_losa="Hormigon", material_tejado="Teja",
    origen=(0, 0, 0)
)

# Parcela de terreno
A.crear_terreno_plano("Parcela", ancho=25.0, fondo=20.0, espesor=0.3, origen=(-12.5, -10, 0), material="Cesped")

# Vegetacion
A.crear_arbol_simple("Arbol_1", radio_copa=2.0, altura_copa=3.5, altura_tronco=2.0, origen=(-8, -6, 0))
A.crear_arbol_simple("Arbol_2", radio_copa=1.5, altura_copa=2.5, altura_tronco=1.5, origen=(7, 4, 0))