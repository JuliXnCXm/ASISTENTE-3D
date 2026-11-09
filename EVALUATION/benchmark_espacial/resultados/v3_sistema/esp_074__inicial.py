import blender_arch as A

A.limpiar_escena()

edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=6,
    ancho=20.0,
    fondo=8.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    origen=(0, 0, 0),
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_marco="Marco_Aluminio"
)

# Girar el edificio 30 grados alrededor del eje Z
A.rotar_objecto(edificio, -30, 'Z')