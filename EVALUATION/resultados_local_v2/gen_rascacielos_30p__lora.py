import blender_arch as A

A.limpiar_escena()

alto_piso = 3.5
num_pisos = 30
ancho_edificio = 24.0

# Crear el volumen principal del edificio
edificio = A.crear_edificio_n_pisos(
    nombre="RascacielosCorporativo",
    pisos=num_pisos,
    ancho=ancho_edificio,
    fondo=ancho_edificio,
    alto_piso=alto_piso,
    grosor_muro=0.3,
    con_techo_plano=True,
    ventanas_fachada=True,
    ventana_ancho=1.8,
    ventana_alto=1.5,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Crear la columna central
A.crear_columna(
    nombre="ColumnaCentral",
    seccion="rect",
    ancho=0.9,
    fondo=0.9,
    alto=alto_piso * num_pisos,
    origen=(ancho_edificio / 2, ancho_edificio / 2, 0),
    material="Acero_Inox"
)