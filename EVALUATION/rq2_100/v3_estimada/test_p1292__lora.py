import blender_arch as A
A.limpiar_escena()
A.crear_terreno_plano('Terreno', ancho=20, fondo=20, material='Asfalto')
A.crear_edificio_n_pisos(
    'Edificio_Oficinas',
    pisos=3,
    ancho=12.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(0, 0, 0),
    material_fachada='Hormigon',
    material_losa='Hormigon',
    material_vidrio='Vidrio_Templado',
    material_marco='Marco_Aluminio'
)
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(-10, -10, 15), energia=2.5)