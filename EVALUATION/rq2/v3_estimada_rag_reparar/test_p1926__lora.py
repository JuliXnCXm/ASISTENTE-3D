import blender_arch as A

A.limpiar_escena()

hab = A.crear_estanteria(
    nombre="LibreriaOficina",
    ancho=1.5,
    alto=2.2,
    fondo=0.3,
    num_estantes=6,
    origen=(2.25, 0.1, 0),
    material="Madera"
)

mesa = A.crear_mesa(
    nombre="Escritorio",
    ancho=1.4,
    fondo=0.7,
    alto=0.75,
    origen=(1.3, 1.8, 0),
    material_tablero="Madera_Roble"
)

silla = A.crear_silla(
    nombre="SillaOficina",
    origen=(1.3, 2.5, 0),
    material="Acero_Inox"
)