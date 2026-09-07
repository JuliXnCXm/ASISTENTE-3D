import blender_arch as A

A.limpiar_escena()

# Crear un sofá en el origen
A.crear_sofa(
    nombre="SofaPrincipal",
    ancho=2.4,
    fondo=0.95,
    alto_asiento=0.45,
    origen=(0, 0, 0),
    material="Tela_Gris"
)

# Crear una mesa de centro enfrente del sofá
A.crear_mesa(
    nombre="MesaCentro",
    ancho=1.2,
    fondo=0.6,
    alto=0.4,
    origen=(0, -1.6, 0),
    material_tablero="Madera"
)