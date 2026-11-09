import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=6,
    ancho=10.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)

# Escalera exterior
A.crear_escalera_recta(
    nombre="EscaleraExterior",
    huella=0.28,
    contrahuella=0.175,
    ancho=1.1,
    num_peldanos=6,
    con_contrahuellas=True,
    origen=(0, -10.0, 0),
    material="Acero_Inox"
)