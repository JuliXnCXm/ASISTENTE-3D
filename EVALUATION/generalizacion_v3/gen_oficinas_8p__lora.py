import blender_arch as A
A.limpiar_escena()

# --- Parámetros ---
ancho_edificio = 20.0
fondo_edificio = 15.0
alto_piso = 3.2
num_pisos = 8

# --- Crear el edificio base ---
edificio = A.crear_edificio_n_pisos(
    nombre="Oficinas_Centrales",
    pisos=num_pisos,
    ancho=ancho_edificio,
    fondo=fondo_edificio,
    alto_piso=alto_piso,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=2.2,
    ventana_alfeizar=0.9,
    ventana_separacion=3.0,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# --- Añadir iluminación y cámara ---
A.agregar_luz(nombre="Luz_Solar", tipo="SUN", ubicacion=(-10, -10, 15), energia=2.5)
A.crear_camara(nombre="Camara_Principal", ubicacion=(10, -12, 8), rotacion=(70, 0, 0))