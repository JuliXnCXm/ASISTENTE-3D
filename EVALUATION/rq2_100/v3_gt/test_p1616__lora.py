import blender_arch as A
A.limpiar_escena()
A.crear_terreno_plano('Base_Asphalt', ancho=50, fondo=50, espesor=0.1, material='Asfalto')
A.crear_edificio_n_pisos(
    'Edificio_Oficinas',
    pisos=5,
    ancho=18.0,
    fondo=12.0,
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
    origen=(0, 0, 0),
    material_fachada='Estuco',
    material_losa='Hormigon',
    material_vidrio='Vidrio_Templado',
    material_marco='Marco_Aluminio'
)
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(-15, -15, 20), energia=2.5)