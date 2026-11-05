import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="TorreOficinas",
    pisos=5,
    ancho=15.0,
    fondo=20.0,
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
    ventana_alfeizar=0.5,
    ventana_separacion=3.0,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Plaza de acceso
A.crear_terreno_plano(
    nombre="PlazaAcceso",
    ancho=15.0,
    fondo=10.0,
    espesor=0.15,
    origen=(0, -10.0, -0.15),
    material="Concreto_Piso"
)