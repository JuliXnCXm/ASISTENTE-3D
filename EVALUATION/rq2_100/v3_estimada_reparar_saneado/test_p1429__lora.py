import blender_arch as A
A.limpiar_escena()

# Plaza de acceso
A.crear_losa_rectangular('Plaza_Acceso', ancho=40.0, fondo=40.0, espesor=0.15, origen=(0, 0, -0.15), material='Concreto_Piso')

# Edificio de oficinas
A.crear_edificio_n_pisos(
    'Edificio_Oficinas',
    pisos=5,
    ancho=18.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.25,
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
    origen=(-9, -7.5, 0),
    material_fachada='Muro_Pintura_Gris',
    material_losa='Hormigon',
    material_vidrio='Vidrio_Templado',
    material_marco='Marco_Aluminio'
)

# Camara y Luz Solar
A.crear_camara('Camara_Principal', ubicacion=(15, -20, 10), rotacion=(70, 0, 135), activa=True)
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(10, -10, 15), energia=2.5)