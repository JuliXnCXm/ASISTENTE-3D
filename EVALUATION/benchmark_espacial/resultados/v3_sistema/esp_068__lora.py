import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioOficinas', pisos=3, ancho=16.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_muro='Muro_Pintura_Gris', material_losa='Hormigon')
origen_x = 8.0
origen_y = 6.0
origen_z = 9.0
volumen_solar = A.extruir_perfil('VolumenSolar', puntos_2d=[(-2.5, -1.5), (-2.5, 1.5), (2.5, 1.5), (2.5, -1.5)], altura=3.0, material='Marco_Aluminio')