import blender_arch as A

A.limpiar_escena()

edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=8,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.25,
    grosor_losa=0.3,
    con_techo_plano=False,
    con_columnas=True,
    seccion_columna="rect",
    dim_columna=(0.4, 0.4),
    modulo_columna_x=4.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=1.8,
    ventana_alfeizar=0.9,
    ventana_separacion=2.4,
    origen=(0, 0, 0),
    material_muro="Muro_Hormigon",
    material_losa="Hormigon",
    material_fachada="Muro_Pintura",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio",
    material_columna="Hormigon"
)