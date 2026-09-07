import blender_arch as A

A.limpiar_escena()

A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.2,
    fondo=0.9,
    alto_asiento=0.42,
    origen=(0, 1.0, 0),
    material="Tela_Gris"
)

A.crear_mesa(
    nombre="Mesa_Centro",
    ancho=1.2,
    fondo=0.6,
    alto=0.45,
    origen=(0, -0.2, 0),
    material_tablero="Madera_Roble"
)