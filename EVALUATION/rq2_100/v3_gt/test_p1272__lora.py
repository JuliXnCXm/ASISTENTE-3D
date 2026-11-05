import blender_arch as A
A.limpiar_escena()
A.crear_piso('Plaza', ancho=20, fondo=15, espesor=0.2, material='Concreto_Piso')
A.crear_edificio_n_pisos(
    'Edificio_Oficinas',
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(0, 0, 0.2),
    material_fachada='Estuco',
    material_losa='Hormigon',
    material_vidrio='Vidrio_Templado',
    material_marco='Marco_Aluminio'
)