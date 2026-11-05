import blender_arch as A

A.limpiar_escena()

muro = A.crear_muro(
    nombre="MuroPerimetral",
    largo=12.0,
    alto=2.2,
    grosor=0.2,
    material="Ladrillo_Rojo"
)

puerta_ancho = 1.0
puerta_alto = 2.0
puerta_grosor = 0.15

centro_vano_x = 12.0 / 2.0
centro_vano_z = puerta_alto / 2.0

A.abrir_vanos_batch_rectangulares(
    muro=muro,
    centros_world=[(centro_vano_x, 0, centro_vano_z)],
    ancho=puerta_ancho,
    alto=puerta_alto
)

A.crear_puerta(
    nombre="PuertaEntrada",
    ancho=puerta_ancho,
    alto=puerta_alto,
    prof_marco=puerta_grosor,
    origen=(centro_vano_x - puerta_ancho / 2.0, 0, 0),
    material_panel="Madera_Roble",
    material_marco="Marco_Negro"
)