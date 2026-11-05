import blender_arch as A

A.limpiar_escena()

# Crear la plaza base
A.crear_terreno_plano(
    nombre="Plaza_Concreto", 
    ancho=40, 
    fondo=40, 
    espesor=0.2, 
    origen=(0, 0, -0.1), 
    material="Concreto_Piso"
)

# Crear el edificio de oficinas
A.crear_edificio_n_pisos(
    nombre="Torre_Oficinas", 
    pisos=5, 
    ancho=18.0, 
    fondo=15.0, 
    alto_piso=3.5, 
    con_columnas=True, 
    dim_columna=0.4,
    modulo_columna_x=6.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True, 
    ventana_ancho=2.2, 
    ventana_alto=2.0, 
    ventana_alfeizar=1.0, 
    ventana_separacion=3.0, 
    origen=(0, 0, 0), 
    material_fachada="Estuco", 
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Negro"
)

# Configurar iluminación y vista
A.agregar_luz("Luz_Sol", tipo="SUN", ubicacion=(15, -25, 30), energia=3.0)
A.crear_camara("Camara_Principal", ubicacion=(30, -35, 20), rotacion=(65, 0, 40), activa=True)