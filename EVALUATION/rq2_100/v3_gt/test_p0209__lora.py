import blender_arch as A

A.limpiar_escena()

# Dimensiones
largo_pared = 3.0
ancho_techo = 1.8
alto_pared = 2.5
grosor_panel_vidrio = 0.02

# Crear la pared trasera
A.crear_muro(
    nombre="ParedTrasera",
    largo=largo_pared,
    alto=alto_pared,
    grosor=0.15,
    origen=(0, 0, 0),
    material="Muro_Pintura"
)

# Crear el techo
A.crear_techo_plano(
    nombre="TechoMarquesina",
    ancho=ancho_techo,
    fondo=largo_pared,
    espesor=0.2,
    origen=(0, 0, alto_pared),
    material="Yeso"
)

# Crear el panel lateral de vidrio
A.crear_losa_rectangular(
    nombre="PanelVidrio",
    ancho=ancho_techo,
    fondo=grosor_panel_vidrio,
    espesor=0.01,
    origen=(0, -largo_pared/2 + grosor_panel_vidrio/2, alto_pared),
    material="Vidrio_Templado"
)