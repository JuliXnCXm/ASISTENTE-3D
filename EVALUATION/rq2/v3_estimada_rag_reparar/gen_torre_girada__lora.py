import blender_arch as A

A.limpiar_escena()

A.crear_torre(
    nombre="TorreResidencial",
    pisos=25,
    ancho=20.0,
    fondo=20.0,
    alto_piso=3.0,
    alto_planta_baja=3.5,
    grosor_losa=0.3,
    modulo_columnas=8.0,
    retiro_columnas=1.0,
    dim_columna=None,
    seccion_columna="rect",
    reducir_columnas=True,
    con_nucleo=False,
    ancho_nucleo=None,
    fondo_nucleo=None,
    grosor_nucleo=0.35,
    fachada="muro_cortina",
    modulo_parteluz=1.5,
    giro_por_piso=2.0,
    escala_superior=1.0,
    con_coronamiento=True,
    origen=(0, 0, 0),
    material_losa="Hormigon",
    material_columna="Hormigon",
    material_nucleo="Hormigon_Nucleo",
    material_vidrio="Vidrio_Templado",
    material_parteluz="Aluminio_Parteluz"
)