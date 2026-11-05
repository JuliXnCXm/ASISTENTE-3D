import blender_arch as A

A.limpiar_escena()

edificio = A.crear_edificio_n_pisos(
    nombre="EdificioApartamentos",
    pisos=5,
    ancho=12.0,
    fondo=15.0,
    alto_piso=2.8,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_techo_plano=True,
    con_columnas=True,
    seccion_columna="rect",
    dim_columna=None,
    modulo_columna_x=4.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.2,
    ventana_alto=1.1,
    ventana_alfeizar=0.9,
    ventana_separacion=2.4,
    origen=(0, 0, 0),
    material_muro="Estuco_Blanco",
    material_losa="Hormigon",
    material_fachada="Estuco_Blanco",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio",
    material_columna="Hormigon"
)