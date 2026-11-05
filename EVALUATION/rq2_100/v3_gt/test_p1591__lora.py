import blender_arch as A
A.limpiar_escena()

# Plaza de acceso
A.crear_terreno_plano(
    nombre="Plaza_Peatonal",
    ancho=30.0,
    fondo=20.0,
    espesor=0.2,
    origen=(0, 0, -0.1),
    material="Concreto_Piso"
)

# Edificio de oficinas
A.crear_edificio_n_pisos(
    nombre="Torre_Oficinas",
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
    ventana_ancho=1.8,
    ventana_alto=2.2,
    ventana_alfeizar=0.6,
    ventana_separacion=2.5,
    origen=(-10, -7.5, 0),
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Iluminación solar
A.agregar_luz(
    nombre="Sol",
    tipo="SUN",
    ubicacion=(15, -15, 25),
    energia=2.5
)