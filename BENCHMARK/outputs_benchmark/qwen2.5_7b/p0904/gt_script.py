import blender_arch as A

A.limpiar_escena()

cama = A.crear_cama(
    nombre="CamaMatrimonio", 
    ancho=1.6, 
    largo=2.0, 
    alto_cabecero=1.2, 
    origen=(0, 0, 0),
    material_colchon="Textil_Blanco", 
    material_base="Madera_Nogal"
)