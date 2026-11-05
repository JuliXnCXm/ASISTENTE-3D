import blender_arch as A

A.limpiar_escena()

estanteria = A.crear_estanteria(
    nombre="EstanteriaPrincipal",
    ancho=1.0,
    alto=1.8,
    fondo=0.3,
    num_estantes=5,
    origen=(0, 0, 0),
    material="Madera_Roble"
)