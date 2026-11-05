import blender_arch as A

A.limpiar_escena()

A.crear_torre_n_pisos(
    nombre="TorreResidencial",
    pisos=25,
    ancho=20.0,
    fondo=20.0,
    alto_piso=3.0,
    rotacion_z=2.0,
    material="Hormigon"
)