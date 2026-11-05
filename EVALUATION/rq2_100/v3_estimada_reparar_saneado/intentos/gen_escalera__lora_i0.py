import blender_arch as A

A.limpiar_escena()

A.crear_escalera_recta(
    nombre="Escalera_Principal",
    huella=0.28,
    contrahuella=0.175,
    ancho=1.1,
    num_peldanos=14,
    con_contrahuellas=True,
    con_zancas=False,
    origen=(0, 0, 0),
    material="Madera"
)

A.crear_baranda_lineal(
    nombre="Baranda_Izquierda",
    largo=14 * 0.28,
    altura=0.95,
    origen=(-14 * 0.28 / 2, -0.1, 0.175),
    material="Acero_Inox"
)

A.crear_baranda_lineal(
    nombre="Baranda_Derecha",
    largo=14 * 0.28,
    altura=0.95,
    origen=(14 * 0.28 / 2, 0.1, 0.175),
    material="Acero_Inox"
)