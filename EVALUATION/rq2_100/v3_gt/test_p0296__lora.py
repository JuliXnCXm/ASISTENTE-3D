import blender_arch as A

A.limpiar_escena()

A.crear_escalera_recta(
    nombre="EscaleraExterior",
    huella=0.3,
    contrahuella=0.18,
    ancho=1.2,
    num_peldanos=12,
    con_contrahuellas=True,
    origen=(0, 0, 0),
    material="Hormigon"
)