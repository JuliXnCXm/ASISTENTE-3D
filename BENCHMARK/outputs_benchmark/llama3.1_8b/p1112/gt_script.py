import blender_arch as A

A.limpiar_escena()

# Crear el sofá principal
A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.4,
    fondo=0.95,
    alto_asiento=0.42,
    origen=(0, 0, 0),
    material="Tela_Gris"
)

# Crear la mesa de centro posicionada frente al sofá
A.crear_mesa(
    nombre="Mesa_Centro",
    ancho=1.2,
    fondo=0.6,
    alto=0.45,
    origen=(0, -1.2, 0),
    material_tablero="Madera_Nogal"
)