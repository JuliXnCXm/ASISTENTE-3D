import blender_arch as A

A.limpiar_escena()

A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=3,
    ancho=15.0,
    fondo=12.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(0, 0, 0),
    material_fachada="Hormigon",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Agregar una base de terreno para el edificio
A.crear_terreno_plano(nombre="Acera", ancho=25, fondo=20, espesor=0.15, origen=(-5, -4, -0.15), material="Asfalto")