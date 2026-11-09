import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioOficinas', pisos=4, ancho=10.0, fondo=8.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_muro='Muro_Pintura_Gris', material_losa='Hormigon')
vol_sobre_cubierta = A.crear_muro(nombre='VolumenSobreCubierta', alto=2.5, origen=(10.0 / 2 - 1.5, 8.0 / 2 - 2.0, 3.0 * 4), material='Muro_Pintura_Gris')