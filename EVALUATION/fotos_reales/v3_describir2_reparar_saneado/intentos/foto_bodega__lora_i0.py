import blender_arch as A

A.limpiar_escena()

# Edificio tipo fábrica o almacén
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioIndustrial",
    pisos=3,
    ancho=25.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=False,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    material_fachada="Ladrillo",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Negro"
)

# Chimenea central
A.crear_columna("Chimenea", seccion="rect", ancho=1.2, fondo=1.2, alto=9.0, origen=(12.4, 7.4, 0), material="Ladrillo")

# Columnas laterales
A.crear_columna("ColumnaIzq", seccion="rect", ancho=0.4, fondo=0.4, alto=9.0, origen=(0.8, 7.4, 0), material="Hormigon")
A.crear_columna("ColumnaDer", seccion="rect", ancho=0.4, fondo=0.4, alto=9.0, origen=(24.8, 7.4, 0), material="Hormigon")