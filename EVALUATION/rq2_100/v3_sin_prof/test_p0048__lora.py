import blender_arch as A

A.limpiar_escena()

# Crear el falso techo
A.crear_techo_reticular(
    nombre="TechoReticular",
    ancho=6.0,
    fondo=4.0,
    espesor=0.05,
    num_paneles_x=6,
    num_paneles_y=4,
    origen=(0, 0, 2.8),
    material="Madera"
)

# Añadir iluminación
A.agregar_luz(
    nombre="Luz1", 
    tipo="POINT", 
    ubicacion=(-2, 2, 3), 
    energia=150
)
A.agregar_luz(
    nombre="Luz2", 
    tipo="POINT", 
    ubicacion=(2, -2, 3), 
    energia=150
)
A.agregar_luz(
    nombre="Luz3", 
    tipo="POINT", 
    ubicacion=(2, 2, 3), 
    energia=150
)
A.agregar_luz(
    nombre="Luz4", 
    tipo="POINT", 
    ubicacion=(-2, -2, 3), 
    energia=150
)