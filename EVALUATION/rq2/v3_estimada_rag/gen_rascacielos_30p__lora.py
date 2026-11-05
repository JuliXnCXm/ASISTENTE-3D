import blender_arch as A

A.limpiar_escena()

A.crear_torre(
    nombre="Rascacielos_Cuadrado",
    pisos=30,
    ancho=24.0,
    fondo=24.0,
    alto_piso=3.6,
    alto_planta_baja=5.0,
    grosor_losa=0.3,
    modulo_columnas=8.0,
    retiro_columnas=1.0,
    dim_columna=None,
    seccion_columna='rect',
    reducir_columnas=True,
    con_nucleo=True,
    ancho_nucleo=6.0,
    fondo_nucleo=6.0,
    grosor_nucleo=0.35,
    fachada='muro_cortina',
    modulo_parteluz=1.5,
    giro_por_piso=0.0,
    escala_superior=1.0,
    con_coronamiento=True,
    origen=(0, 0, 0),
    material_losa="Hormigon",
    material_columna="Hormigon",
    material_nucleo="Hormigon_Nucleo",
    material_vidrio="Vidrio_Templado",
    material_parteluz="Aluminio_Parteluz"
)