import blender_arch as A

A.limpiar_escena()

# Edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=3,
    ancho=16.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Volumen sobre la cubierta
volumen_solar = A.crear_volumen(
    nombre="VolumenSolar",
    ancho=5.0,
    fondo=3.0,
    alto=3.0,
    origen=(8.0, 6.0, 9.0), # Centrado sobre la cubierta (16/2 - 5/2, 12/2 - 3/2, 3*3)
    material="Marco_Aluminio"
)