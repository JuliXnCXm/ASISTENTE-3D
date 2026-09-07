import blender_arch as A

A.limpiar_escena()

A.crear_cama(
    nombre="CamaDoble",
    ancho=1.6,
    largo=2.0,
    alto_cabecero=1.0,
    origen=(0, 0, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Nogal"
)