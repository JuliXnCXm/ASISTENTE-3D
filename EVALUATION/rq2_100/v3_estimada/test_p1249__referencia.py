import blender_arch as A

A.limpiar_escena()

A.crear_terreno_plano(
    nombre="PlataformaEdificio",
    ancho=25.0,
    fondo=22.0,
    espesor=0.2,
    material="Concreto_Piso",
    origen=(0, 0, -0.2)
)

A.crear_edificio_n_pisos(
    nombre="OficinasCentrales",
    pisos=4,
    ancho=15.0,
    fondo=12.0,
    alto_piso=3.2,
    grosor_muro=0.25,
    con_techo_plano=True,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(0, 0, 0),
    material_fachada="Estuco",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

A.agregar_luz(
    nombre="LuzSolar",
    tipo="SUN",
    ubicacion=(15, -20, 30),
    energia=2.5,
    color=(1.0, 0.9, 0.8)
)