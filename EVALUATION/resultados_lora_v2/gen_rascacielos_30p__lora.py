import blender_arch as A

A.limpiar_escena()

# Crear el edificio principal
edificio = A.crear_edificio_n_pisos(
    nombre="Rascacielos",
    pisos=30,
    ancho=24.0,
    fondo=24.0,
    alto_piso=3.5,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=6.0,
    modulo_columna_y=6.0,
    ventanas_fachada=True,
    ventana_ancho=2.8,
    ventana_alto=2.2,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    material_fachada="Vidrio_Templado",
    material_losa="Hormigon",
    material_vidrio="Vidrio",
    material_marco="Marco_Aluminio"
)

# Añadir iluminación y cámara
A.agregar_luz(nombre="Luz_Solar", tipo="SUN", ubicacion=(-10, -10, 20), energia=2.5)
A.crear_camara(nombre="Camara_Principal", ubicacion=(15, -15, 10), rotacion=(70, 0, 0))