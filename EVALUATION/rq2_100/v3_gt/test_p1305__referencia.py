import blender_arch as A

A.limpiar_escena()

ancho_puerta = 1.0
alto_puerta = 2.0
largo_muro = 12.0

muro = A.crear_muro(
    nombre="Muro.Perimetro",
    largo=largo_muro,
    alto=2.2,
    grosor=0.25,
    material="Ladrillo_Rojo"
)

centro_x = largo_muro / 2

A.crear_puerta(
    nombre="Puerta.Jardin",
    ancho=ancho_puerta,
    alto=alto_puerta,
    origen=(centro_x, 0, 0),
    material_panel="Madera",
    material_marco="Marco_Negro"
)

A.abrir_vanos_batch_rectangulares(
    muro=muro,
    centros_world=[(centro_x, 0, alto_puerta / 2)],
    ancho=ancho_puerta,
    alto=alto_puerta
)