import blender_arch as A

A.limpiar_escena()

A.crear_escalera_spiral(
    nombre="Escalera_Caracol",
    huella=0.28,
    contrahuella=0.18,
    ancho=0.9,
    num_peldanos=16,
    radio=0.9,
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