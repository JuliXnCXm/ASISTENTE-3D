import blender_arch as A
A.limpiar_escena()
A.crear_terreno_plano(nombre='Plaza_Concreto', ancho=40.0, fondo=30.0, espesor=0.2, material='Concreto_Piso')
A.crear_edificio_n_pisos(
    nombre='Oficinas_Centrales',
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=False,
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
A.agregar_luz(nombre='Luz_Solar', tipo='SUN', ubicacion=(-15, -20, 25), energia=2.5)