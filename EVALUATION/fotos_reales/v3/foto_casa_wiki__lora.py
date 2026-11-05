import blender_arch as A
A.limpiar_escena()

# Casa tipo Villa con patio
casa = A.crear_casa_n_pisos(
    nombre="Villa_Familiar",
    pisos=2,
    ancho=16.8, fondo=13.7, alto_piso=2.9,
    grosor_muro=0.2, grosor_losa=0.2,
    con_tejado=True, altura_cumbrera=2.5, voladizo=0.6,
    material_muro="Estuco", material_losa="Hormigon", material_tejado="Teja",
    origen=(0, 0, 0)
)

# Mobiliario exterior
A.crear_área_con_huecos("Zona_Parque", ancho=16.8, fondo=13.7, agujeros=[[(0, 0, 0), (16.8, 13.7, 0.2)]], material="Cesped")
A.crear_pavimento("Pavimento_Parque", ancho=16.8, fondo=13.7, origen=(0, 0, -0.2), material="Asfalto")

A.crear_arbol_simple("Arbol_1", origen=(10, 12, 0))
A.crear_arbol_simple("Arbol_2", origen=(5, 5, 0))

# Mobiliario interior
A.crear_puerta("Puerta_Principal", ancho=2.1, alto=2.1, origen=(3.3, 0.1, 0), material_panel="Madera_Roble", material_marco="Marco_Negro")
A.crear_puerta("Puerta_Servicio", ancho=1.0, alto=2.1, origen=(15.3, 0.1, 0), material_panel="Madera_Roble", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente", ancho=5.4, alto=1.8, origen=(3.3, 2.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente_2", ancho=5.4, alto=1.8, origen=(11.4, 2.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente_3", ancho=5.4, alto=1.8, origen=(17.4, 2.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente_4", ancho=5.4, alto=1.8, origen=(3.3, 6.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente_5", ancho=5.4, alto=1.8, origen=(11.4, 6.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente_6", ancho=5.4, alto=1.8, origen=(17.4, 6.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente_7", ancho=5.4, alto=1.8, origen=(3.3, 10.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente_8", ancho=5.4, alto=1.8, origen=(11.4, 10.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")
A.crear_ventana("Ventana_Frente_9", ancho=5.4, alto=1.8, origen=(17.4, 10.2, 0), material_vidrio="Vidrio", material_marco="Marco_Negro")