import blender_arch as A

A.limpiar_escena()

A.crear_escalera_recta(
    nombre="EscaleraPrincipal",
    huella=0.28,
    contrahuella=0.175,
    ancho=1.1,
    num_peldanos=14,
    con_contrahuellas=True,
    origen=(0, 0, 0),
    material="Hormigon"
)

A.crear_baranda_lineal(
    nombre="BarandaIzquierda",
    largo=14 * 0.28 + 1.5, # 1.5m de espacio
    altura=1.0,
    poste_cada=1.0,
    origen=(-1.5, -0.2, 0.175), # 0.175m de contrahuella
    material="Acero_Inox"
)

A.crear_baranda_lineal(
    nombre="BarandaDerecha",
    largo=14 * 0.28 + 1.5, # 1.5m de espacio
    altura=1.0,
    poste_cada=1.0,
    origen=(1.5, 0.2, 0.175), # 0.175m de contrahuella
    material="Acero_Inox"
)