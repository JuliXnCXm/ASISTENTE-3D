import blender_arch as A
A.limpiar_escena()
A.crear_terreno_plano(nombre='Base_Hormigon', ancho=30, fondo=30, espesor=0.2, material='Concreto_Piso')
A.crear_edificio_n_pisos(
    nombre='Oficinas_Centrales',
    pisos=4,
    ancho=15.0,
    fondo=12.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
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
A.agregar_luz(nombre='Luz_Solar', tipo='SUN', ubicacion=(-10, -10, 20), energia=2.5)