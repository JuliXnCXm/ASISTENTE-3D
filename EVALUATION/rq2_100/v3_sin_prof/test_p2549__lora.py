import blender_arch as A

A.limpiar_escena()

A.crear_escalera_caracol(
    nombre="EscaleraPrincipal",
    huella=0.28,
    contrahuella=0.175,
    ancho=1.0,
    num_peldanos=16,
    radio=0.9,
    altura_total=3.0,
    con_contrahuellas=True,
    origen=(0, 0, 0),
    material="Madera"
)

A.crear_columna(
    nombre="PosteCentral",
    seccion="circ",
    diametro=0.2,
    alto=3.0,
    origen=(0, 0, 0),
    material="Hormigon"
)