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
    centros_world=[(-2.5 + i/2, 0.15, 1.2) for i in range(8)],
    ancho=1.2,
    alto=1.5
)