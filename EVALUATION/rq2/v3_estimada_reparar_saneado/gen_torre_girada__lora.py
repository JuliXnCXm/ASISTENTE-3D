import blender_arch as A
A.limpiar_escena()
A.crear_edificio_n_pisos(nombre='TorreResidencial', pisos=25, ancho=20.0, fondo=20.0, alto_piso=3.0, grosor_muro=0.3, con_techo_plano=True, origen=(0, 0, 0), material_muro='Hormigon')
A.asignar_rotacion_z('TorreResidencial', angulo_rad=2 * 3.14159 / 25)