import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas contemporáneo
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioContemporaneo",
    pisos=2,
    ancho=10.0,
    fondo=15.0,
    alto_piso=2.8,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_techo_plano=True,
    con_columnas=True,
    seccion_columna="rect",
    dim_columna=(0.4, 0.4),
    modulo_columna_x=4.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.2,
    ventana_alto=1.1,
    ventana_alfeizar=0.9,
    ventana_separacion=2.4,
    origen=(0, 0, 0),
    material_muro="Estuco_Blanco",
    material_losa="Hormigon",
    material_fachada="Marco_Aluminio",
    material_vidrio="Vidrio_Templado"
)

# Muro de celosía en la planta alta
muro_celosia = A.crear_muro(
    nombre="Muro_Celosia",
    largo=10.0,
    alto=2.8,
    grosor=0.15,
    origen=(0, 15.0, 2.8),
    rotacion_z=-90.0,
    material="Madera_Roble"
)

# Ventana grande en la planta alta
ventana_planta_altta = A.crear_ventana(
    nombre="Ventana_PlantaAltta",
    ancho=5.0,
    alto=1.8,
    prof_marco=0.15,
    divisiones=(1, 1),
    origen=(2.0, 15.0, 2.8 + 0.9),
    material_marco="Marco_Negro",
    material_vidrio="Vidrio"
)