import blender_arch as A

A.limpiar_escena()

# Dimensiones
largo_pared = 3.0
ancho_techo = 1.2
alto_pared = 2.5
grosor_panel_vidrio = 0.02

# Crear la pared trasera
A.crear_muro(
    nombre="Pared_Trasera",
    largo=largo_pared,
    alto=alto_pared,
    grosor=0.15,
    origen=(0, 0, 0),
    material="Muro_Pintura"
)

# Crear el techo
A.crear_techo_plano(
    nombre="Techo_Marquesina",
    ancho=largo_pared + 0.3,
    fondo=ancho_techo,
    espesor=0.2,
    origen=(0, -ancho_techo/2, alto_pared),
    material="Yeso"
)

# Crear el panel lateral de vidrio
A.crear_losa_rectangular(
    nombre="Panel_Vidrio",
    ancho=ancho_techo,
    fondo=grosor_panel_vidrio,
    espesor=0.01,
    origen=(0, 0, alto_pared),
    material="Vidrio"
)