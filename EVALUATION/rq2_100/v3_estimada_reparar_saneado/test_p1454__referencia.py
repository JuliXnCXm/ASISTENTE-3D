import blender_arch as A

A.limpiar_escena()

ancho_edificio = 20.0
ancho_puerta = 1.2

edificio = A.crear_edificio_n_pisos(
    nombre='EdificioOficinas',
    pisos=5,
    ancho=ancho_edificio,
    fondo=15.0,
    alto_piso=3.2,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=2.2,
    ventana_alto=2.5,
    ventana_alfeizar=0.4,
    ventana_separacion=2.4,
    material_fachada='Muro_Pintura_Gris',
    material_losa='Hormigon',
    material_vidrio='Vidrio',
    material_marco='Marco_Aluminio'
)

# Crear entrada principal con dos puertas
pos_centro_entrada = ancho_edificio / 2.0

A.crear_puerta(
    'PuertaEntrada_Izq',
    ancho=ancho_puerta,
    alto=2.4,
    origen=(pos_centro_entrada - ancho_puerta, 0, 0),
    material_panel='Vidrio_Templado',
    material_marco='Acero_Inox'
)

A.crear_puerta(
    'PuertaEntrada_Der',
    ancho=ancho_puerta,
    alto=2.4,
    origen=(pos_centro_entrada, 0, 0),
    material_panel='Vidrio_Templado',
    material_marco='Acero_Inox'
)