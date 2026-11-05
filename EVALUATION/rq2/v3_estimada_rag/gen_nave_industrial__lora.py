import blender_arch as A

A.limpiar_escena()

# Edificio tipo nave industrial
edificio = A.crear_edificio_n_pisos(
    nombre="NaveIndustrial",
    pisos=1,
    ancho=30.0,
    fondo=20.0,
    alto_piso=8.0,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_techo_plano=True,
    con_columnas=True,
    seccion_columna="rect",
    dim_columna=(0.4, 0.4),
    modulo_columna_x=6.0,
    modulo_columna_y=6.0,
    origen=(0, 0, 0),
    material_muro="Hormigon",
    material_losa="Hormigon",
    material_techo="Hormigon"
)

# Cubierta plana
A.crear_tejado_dos_aguas(
    nombre="CubiertaPlana",
    ancho=30.0,
    fondo=20.0,
    altura_cumbrera=0.0,
    espesor=0.15,
    voladizo_x=0.0,
    voladizo_y=0.0,
    origen=(0, 0, 8.15),
    material="Hormigon"
)