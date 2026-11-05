import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="TorreOficinas",
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=False,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    material_fachada="Estuco",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Plaza de acceso
A.crear_terreno_plano("PlazaAcceso", ancho=40.0, fondo=30.0, espesor=0.15, origen=(0, 0, -0.15), material="Concreto_Piso")

# Iluminación
A.agregar_luz("LuzSolar", tipo="SUN", ubicacion=(-15, -20, 25), energia=2.5)