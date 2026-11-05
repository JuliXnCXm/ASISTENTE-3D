import blender_arch as A

A.limpiar_escena()

# Crear el edificio principal
edificio = A.crear_edificio_n_pisos(
    nombre="OficinasCentrales",
    pisos=8,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=2.2,
    ventana_alfeizar=0.9,
    ventana_separacion=3.0,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Añadir iluminación y cámara
A.agregar_luz(nombre="LuzPrincipal", tipo="SUN", ubicacion=(-10, -10, 20), energia=2.5)
A.crear_camara(nombre="CamaraFrontal", ubicacion=(0, -15, 8), rotacion=(80, 0, 0))