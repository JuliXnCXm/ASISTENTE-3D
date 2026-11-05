import blender_arch as A

A.limpiar_escena()

A.crear_escalera_spiral(
    nombre="Escalera_Caracol",
    huella=0.28,
    contrahuella=0.18,
    ancho=1.0,
    num_peldanos=16,
    radio_min=0.9,
    radio_max=1.8,
    origen=(0, 0, 0),
    material="Madera"
)

A.crear_columna(
    nombre="Poste_Central",
    seccion="circ",
    diametro=0.2,
    alto=3.0,
    origen=(0, 0, 0),
    material="Hormigon"
)