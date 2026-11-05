import blender_arch as A
A.limpiar_escena()

# Parámetros del edificio
num_pisos = 30
ancho_planta = 24.0
fondo_planta = 24.0
alto_piso = 3.5

# Crear el edificio
edificio = A.crear_edificio_n_pisos(
    nombre="Rascacielos_Centro",
    pisos=num_pisos,
    ancho=ancho_planta,
    fondo=fondo_planta,
    alto_piso=alto_piso,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=6.0,
    modulo_columna_y=6.0,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=2.2,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    material_fachada="Vidrio_Templado",
    material_marco="Marco_Aluminio",
    material_losa="Hormigon",
    material_columna="Hormigon_Visto"
)

# Añadir iluminación y cámara
A.agregar_luz("Luz_Solar", tipo="SUN", ubicacion=(-10, -10, 20), energia=3.0)
A.crear_camara("Camara_Principal", ubicacion=(15, -15, 10), rotacion=(70, 0, 0))