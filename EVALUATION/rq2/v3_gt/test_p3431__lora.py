import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la cocina en L
cocina_l = A.crear_cocina_L(
    ancho=5.0,
    fondo=4.0,
    alto_mesa=0.9,
    origen=(0, 0, 0),
    material_mesa="Cuarzo_Blanco",
    material_piso="Porcelanato"
)

# Añadir mobiliario bajo y alto
A.crear_armario("Armario_Bajo_1", ancho=2.5, alto=0.8, fondo=0.6, origen=(-1.25, 3.2, 0), material="MDF_Blanco")
A.crear_armario("Armario_Bajo_2", ancho=2.5, alto=0.8, fondo=0.6, origen=(1.25, 3.2, 0), material="MDF_Blanco")
A.crear_armario("Armario_Alto_1", ancho=2.5, alto=1.8, fondo=0.6, origen=(-1.25, 3.2, 1.0), material="MDF_Blanco")
A.crear_armario("Armario_Alto_2", ancho=2.5, alto=1.8, fondo=0.6, origen=(1.25, 3.2, 1.0), material="MDF_Blanco")

# Crear la isla central
isla_ancho = 2.0
isla_fondo = 1.0
isla_alto = 0.9
isla_origen = (0, 1.5, 0)
A.crear_mesa("Isla_Central", ancho=isla_ancho, fondo=isla_fondo, alto=isla_alto, origen=isla_origen, material_tablero="Acero_Inox")

# Añadir mobiliario de la isla
taburete1 = A.crear_silla("Taburete_Isla_1", origen=(isla_ancho/2 - 0.4, 0.2, 0), material="Cuero")
taburete2 = A.crear_silla("Taburete_Isla_2", origen=(isla_ancho/2 + 0.4, 0.2, 0), material="Cuero")

# Instalar el extractor sobre la zona de cocción
extractor_origen = (0, 1.5, 0.9)
A.crear_ventana("Extractor", ancho=0.9, alto=0.6, prof_marco=0.1, origen=extractor_origen, material_marco="Marco_Negro", material_vidrio="Vidrio_Templado")

# Iluminación y cámara
A.agregar_luz("Luz_Principal", tipo="AREA", ubicacion=(0, 0, 3.5), energia=800)
A.crear_camara("Camara", ubicacion=(0, -5, 2.5), rotacion=(80, 0, 0))