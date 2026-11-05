import blender_arch as A

A.limpiar_escena()

# Edificio de 2 pisos con planta baja abierta
edificio = A.crear_edificio_n_pisos(
    nombre="ViviendaMinimalista",
    pisos=2,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    grosor_muro=0.2,
    grosor_losa=0.2,
    con_techo_plano=True,
    con_columnas=False,
    origen=(0, 0, 0),
    material_muro="Hormigon",
    material_losa="Hormigon",
    material_fachada="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio",
    material_columna="Hormigon"
)

# Cubierta plana y transitable
techo_plano = A.crear_techo_plano(
    nombre="CubiertaTransitable",
    ancho=10.0,
    fondo=8.0,
    espesor=0.2,
    origen=(0, 0, 5.6)
)