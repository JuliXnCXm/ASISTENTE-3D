import blender_arch as A

A.limpiar_escena()

# Crear un sofá de 2.2 metros de ancho
A.crear_sofa(
    nombre="Sofa_Principal", 
    ancho=2.2, 
    fondo=0.95, 
    alto_asiento=0.42, 
    origen=(0, 0, 0), 
    material="Tela_Gris"
)

# Crear una mesa de centro frente al sofá
A.crear_mesa(
    nombre="Mesa_Centro", 
    ancho=1.2, 
    fondo=0.6, 
    alto=0.4, 
    origen=(0.5, -1.2, 0), 
    material_tablero="Madera_Nogal"
)