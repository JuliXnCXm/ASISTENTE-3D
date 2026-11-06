import blender_arch as A

A.limpiar_escena()

# Edificio tipo fábrica o almacén
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioIndustrial",
    pisos=2,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=4.0,
    material_fachada="Ladrillo",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Negro"
)

# Chimeneas centrales
A.crear_columna("Chimenea_Izq", seccion="circ", diametro=1.2, alto=12.0, origen=(-7, -7, 0), material="Ladrillo")
A.crear_columna("Chimenea_Der", seccion="circ", diametro=1.2, alto=12.0, origen=(7, -7, 0), material="Ladrillo")

# Puerta principal
A.crear_puerta("Puerta_Acceso", ancho=3.0, alto=2.2, prof_marco=0.3, origen=(0, -1.5, 0), material_panel="Acero_Inox", material_marco="Acero_Inox")

# Suelo
A.crear_terreno_plano("Suelo_Camino", ancho=40, fondo=30, espesor=0.15, origen=(-20, -15, -0.15), material="Asfalto")

# Mobiliario exterior
A.crear_mesa("Mesa_1", ancho=2.5, fondo=1.2, alto=0.75, origen=(0, 10, 0), material_tablero="Madera_Roble", material_patas="Metal_Negro")
A.crear_mesa("Mesa_2", ancho=2.5, fondo=1.2, alto=0.75, origen=(0, 15, 0), material_tablero="Madera_Roble", material_patas="Metal_Negro")
A.crear_silla("Silla_1", origen=(0, 10, 0), material="Cuero")
A.crear_silla("Silla_2", origen=(0, 12, 0), material="Cuero")
A.crear_silla("Silla_3", origen=(0, 14, 0), material="Cuero")