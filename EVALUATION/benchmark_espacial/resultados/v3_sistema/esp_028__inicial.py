import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=5,
    ancho=18.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)

# Escalera exterior en la fachada oeste (Y+)
A.crear_escalera_recta(
    nombre="Escalera_Exterior",
    huella=0.28,
    contrahuella=0.175,
    ancho=1.1,
    num_peldanos=5,
    origen=(0, -5.0, 0), # Centrado en Y, en el suelo
    material="Acero_Inox"
)