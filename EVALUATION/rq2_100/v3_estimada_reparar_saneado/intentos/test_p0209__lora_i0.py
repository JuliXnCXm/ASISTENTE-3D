import blender_arch as A

A.limpiar_escena()

# Dimensiones
largo_pared = 3.0
ancho_techo = 1.5
alto_techo = 2.5
grosor_muro = 0.15
ancho_vidrio = 1.0

# Crear la pared trasera
A.crear_muro(
    nombre="Pared_Trasera",
    largo=largo_pared,
    alto=alto_techo,
    grosor=grosor_muro,
    origen=(0, 0, 0),
    material="Muro_Pintura"
)

# Crear el techo
A.crear_techo_plano(
    nombre="Techo_Marquesina",
    ancho=ancho_techo,
    fondo=largo_pared,
    espesor=0.2,
    origen=(0, -grosor_muro/2, alto_techo),
    material="Yeso"
)

# Crear el panel lateral de vidrio
A.crear_ventana(
    nombre="Panel_Vidrio",
    ancho=ancho_vidrio,
    alto=alto_techo,
    prof_marco=grosor_muro,
    divisiones=(1, 1),
    origen=(-grosor_muro/2, 0, 0),
    material_marco="Marco_Negro",
    material_vidrio="Vidrio"
)