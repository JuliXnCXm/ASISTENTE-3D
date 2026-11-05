import blender_arch as A

A.limpiar_escena()

# Muro base de la planta baja
muro_p1 = A.crear_muro(
    nombre="Muro_P1",
    largo=10.0,
    alto=2.8,
    grosor=0.3,
    material="Hormigon"
)

# Muro de la planta alta, retranqueado
muro_p2 = A.crear_muro(
    nombre="Muro_P2",
    largo=10.0,
    alto=2.8,
    grosor=0.3,
    origen=(0, -1.0, 2.8),
    material="Hormigon"
)

# Ventana de la planta alta
ventana_p2 = A.crear_ventana(
    nombre="Ventana_P2",
    ancho=9.0,
    alto=2.7,
    prof_marco=0.3,
    divisiones=(3, 2),
    origen=(0, -1.0, 2.8),
    material_marco="Marco_Negro",
    material_vidrio="Vidrio"
)

# Cubierta plana y transitable
cubierta = A.crear_techo_plano(
    nombre="Cubierta_P2",
    ancho=10.0,
    fondo=10.0,
    espesor=0.2,
    origen=(0, -1.0, 5.6),
    material="Hormigon"
)