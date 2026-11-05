import blender_arch as A

A.limpiar_escena()

muro = A.crear_muro(
    nombre="MuroPerimetral",
    largo=8.0,
    alto=2.2,
    grosor=0.2,
    material="Ladrillo_Rojo"
)

puerta_ancho = 1.0
puerta_alto = 2.0
puerta_origen_x = (8.0 - puerta_ancho) / 2

A.crear_puerta(
    nombre="PuertaAcceso",
    ancho=puerta_ancho,
    alto=puerta_alto,
    prof_marco=0.2,
    origen=(puerta_origen_x, 0, 0),
    material_panel="Madera_Roble",
    material_marco="Marco_Negro"
)