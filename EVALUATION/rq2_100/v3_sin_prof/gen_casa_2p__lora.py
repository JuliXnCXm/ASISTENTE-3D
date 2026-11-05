import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA ---
casa = A.crear_casa_n_pisos(
    nombre="CasaFamiliar",
    pisos=2,
    ancho=8.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# --- VENTANAS Y PUERTA ---
ventana_ancho = 1.5
ventana_alto = 1.8
ventana_alfeizar = 0.9

# Ventanas en la fachada frontal (Y=0)
A.crear_ventana(
    nombre="Ventana_Frente_1",
    ancho=ventana_ancho,
    alto=ventana_alto,
    prof_marco=0.2,
    origen=(2.0 + ventana_ancho/2, -0.1, 0.9),
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)

A.crear_ventana(
    nombre="Ventana_Frente_2",
    ancho=ventana_ancho,
    alto=ventana_alto,
    prof_marco=0.2,
    origen=(8.0 - ventana_ancho/2, -0.1, 0.9),
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)

# Puerta en la fachada frontal (Y=0)
puerta_ancho = 1.0
puerta_alto = 2.1
puerta_prof_marco = 0.2

A.crear_puerta(
    nombre="Puerta_Principal",
    ancho=puerta_ancho,
    alto=puerta_alto,
    prof_marco=puerta_prof_marco,
    origen=(4.0, -0.1, 0.0),
    material_panel="Madera_Roble",
    material_marco="Marco_Negro"
)

# --- ILUMINACION Y CÁMARA ---
A.agregar_luz(nombre="Luz_Solar", tipo="SUN", ubicacion=(-5, -10, 10), energia=2.5)
A.crear_camara(nombre="Camara_Frontal", ubicacion=(0, -12, 5), rotacion=(75, 0, 0))