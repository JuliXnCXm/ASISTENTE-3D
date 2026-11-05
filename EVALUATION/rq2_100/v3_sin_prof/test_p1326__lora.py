import blender_arch as A
A.limpiar_escena()
A.crear_terreno_plano('Jardin', ancho=20, fondo=15, espesor=0.2, material='Cesped')
A.crear_casa_n_pisos(
    'CasaCampo',
    pisos=2,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    origen=(0, 0, 0.2),
    material_muro='Estuco',
    material_tejado='Teja'
)
A.crear_losa_rectangular('CaminoAcceso', ancho=4.0, fondo=0.1, espesor=0.15, origen=(-6, -7, 0.2), material='Concreto_Piso')