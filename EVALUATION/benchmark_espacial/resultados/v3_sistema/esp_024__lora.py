import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=4,
    ancho=16.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Escalera exterior en el lado Norte (Y+)
A.crear_escalera_recta(
    nombre="Escalera_Exterior",
    huella=0.28,
    contrahuella=0.175,
    ancho=1.1,
    num_peldanos=4,
    origen=(0, -12/2 + 0.25/2 + 1.1/2, 0),
    material="Acero_Inox"
)