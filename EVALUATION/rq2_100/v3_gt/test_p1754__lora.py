import blender_arch as A
A.limpiar_escena()
A.crear_terreno_plano('Parcela', ancho=20, fondo=15, espesor=0.2, material='Cesped')
A.crear_casa_n_pisos(
    'Casa_Familiar',
    pisos=2,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    origen=(0, 0, 0.1),
    material_muro='Ladrillo_Rojo',
    material_losa='Hormigon',
    material_tejado='Teja'
)
A.crear_arbol_simple('Arbol_1', origen=(-4, -3, 0))
A.crear_arbol_simple('Arbol_2', radio_copa=2.0, altura_copa=3.5, origen=(4, 2, 0))