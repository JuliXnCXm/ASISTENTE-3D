import blender_arch as A

A.limpiar_escena()

A.crear_terreno_plano(
    nombre="BaseUrbana",
    ancho=50.0,
    fondo=50.0,
    material="Asfalto"
)

A.crear_edificio_n_pisos(
    nombre='OficinasCentrales',
    pisos=5,
    ancho=24.0,
    fondo=18.0,
    alto_piso=3.2,
    con_columnas=True,
    dim_columna=0.5,
    modulo_columna_x=6.0,
    modulo_columna_y=6.0,
    ventanas_fachada=True,
    ventana_ancho=1.8,
    ventana_alto=1.6,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(0, 0, 0),
    material_fachada='Estuco',
    material_losa='Hormigon',
    material_vidrio='Vidrio_Templado',
    material_marco='Marco_Aluminio'
)