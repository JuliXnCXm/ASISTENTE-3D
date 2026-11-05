import blender_arch as A

A.limpiar_escena()

# Crear un terreno base que simule asfalto o una plaza
A.crear_terreno_plano(
    nombre="Plaza_Edificio",
    ancho=40,
    fondo=40,
    espesor=0.2,
    origen=(20, 20, -0.1),
    material="Asfalto"
)

# Crear el edificio de oficinas con ventanas en la fachada
A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=3,
    ancho=12.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    ventanas_fachada=True,
    ventana_ancho=1.8,
    ventana_alto=1.5,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(20, 20, 0),
    material_fachada="Hormigon",
    material_losa="Concreto_Piso",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Añadir una luz solar para iluminar la escena exterior
A.agregar_luz(
    nombre="Luz_Principal",
    tipo="SUN",
    ubicacion=(15, -25, 30),
    energia=3.0
)