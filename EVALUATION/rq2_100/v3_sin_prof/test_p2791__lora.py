import blender_arch as A

A.limpiar_escena()

fachada = A.crear_muro(
    nombre="Fachada_Principal",
    largo=10.0,
    alto=6.0,
    grosor=0.3,
    material="Muro_Pintura_Gris"
)

A.abrir_vanos_batch_rectangulares(
    muro=fachada,
    centros_world=[(0, 0, 1.8), (0, 0, 3.6)],
    ancho=0.9,
    alto=1.2
)