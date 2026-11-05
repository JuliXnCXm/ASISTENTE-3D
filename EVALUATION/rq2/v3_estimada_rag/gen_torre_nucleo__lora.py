import blender_arch as A

A.limpiar_escena()

# Crear la torre principal
A.crear_torre(
    nombre="TorrePrincipal",
    pisos=20,
    ancho=30.0,
    fondo=30.0,
    alto_piso=3.6,
    alto_planta_baja=5.0,
    grosor_losa=0.3,
    modulo_columnas=8.0,
    retiro_columnas=1.0,
    dim_columna=(0.4, 0.4),
    seccion_columna="rect",
    reducir_columnas=True,
    con_nucleo=True,
    ancho_nucleo=10.0,
    fondo_nucleo=10.0,
    grosor_nucleo=0.35,
    fachada="muro_cortina",
    modulo_parteluz=1.5,
    giro_por_piso=0.0,
    escala_superior=1.0,
    con_coronamiento=False,
    origen=(0, 0, 0),
    material_losa="Hormigon",
    material_columna="Hormigon",
    material_nucleo="Hormigon_Nucleo",
    material_vidrio="Vidrio_Templado",
    material_parteluz="Marco_Aluminio"
)

# Crear el muro de fachada exterior
A.crear_muro(
    nombre="FachadaExterior",
    largo=30.0,
    alto=3.6 * 20 + 5.0,
    grosor=0.2,
    origen=(-15.0, -15.0, 0),
    rotacion_z=0.0,
    material="Marco_Aluminio"
)

# Abrir vanos para las ventanas en el muro de fachada
muro_fachada = A.obtener_objeto("FachadaExterior")
A.abrir_vanos_grid_local(
    muro=muro_fachada,
    filas=20,
    cols=1,
    x0=-15.0,
    z0=5.0,
    dx=30.0,
    dz=3.6,
    ancho=1.2,
    alto=1.1,
    profundidad=None,
    nombre="VentanasGrid",
    aplicar=True
)