import blender_arch as A

A.limpiar_escena()

edificio = A.crear_edificio_n_pisos(
    nombre='Oficinas_Corporativas',
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.5,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.5,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=2.2,
    ventana_alfeizar=0.9,
    ventana_separacion=2.5,
    material_fachada='Muro_Pintura_Gris',
    material_losa='Hormigon',
    material_vidrio='Vidrio_Templado',
    material_marco='Marco_Aluminio'
)