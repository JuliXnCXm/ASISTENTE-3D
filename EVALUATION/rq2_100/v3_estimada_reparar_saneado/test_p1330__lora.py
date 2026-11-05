import blender_arch as A
A.limpiar_escena()
terreno = A.crear_terreno_plano(nombre='Parcela', ancho=20, fondo=16, espesor=0.2, material='Cesped')
casa_datos = {'nombre': 'Casa_Familiar', 'ancho': 10.0, 'fondo': 8.0, 'alto_piso': 2.8, 'num_pisos': 2, 'grosor_muro': 0.2, 'voladizo': 0.5, 'origen': (0, 0, 0.1), 'material_muro': 'Ladrillo_Rojo', 'material_losa': 'Hormigon', 'material_tejado': 'Teja'}
A.crear_casa_n_pisos(**casa_datos)
A.crear_arbol_simple(nombre='Arbol_1', radio_copa=1.5, altura_copa=3.0, altura_tronco=1.8, origen=(-4, -3, 0.1))
A.crear_arbol_simple(nombre='Arbol_2', radio_copa=1.2, altura_copa=2.5, altura_tronco=1.5, origen=(4, 2, 0.1))