import blender_arch as A
A.limpiar_escena()

# Casa tipo Villa con parámetros modificados
casa = A.crear_casa_n_pisos(
    nombre="CasaFamiliar",
    pisos=2,
    ancho=10.0, fondo=9.0, alto_piso=2.8,
    grosor_muro=0.2, grosor_losa=0.2,
    con_tejado=True, altura_cumbrera=2.0, voladizo=0.5,
    material_muro="Ladrillo", material_losa="Hormigon", material_tejado="Teja",
    origen=(0, 0, 0)
)

# Parcela alrededor de la casa
A.crear_terreno_plano("Parcela", ancho=25.0, fondo=20.0, espesor=0.3, origen=(-12.5, -10, 0), material="Cesped")

# Vegetación en el jardín frontal
A.crear_arbol_simple("Arbol_1", radio_copa=1.2, altura_copa=3.0, altura_tronco=1.8, origen=(-3, -2, 0))
A.crear_arbol_simple("Arbol_2", radio_copa=1.0, altura_copa=2.5, altura_tronco=1.5, origen=(3, -2, 0))