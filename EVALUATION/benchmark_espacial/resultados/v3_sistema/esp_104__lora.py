import blender_arch as A
A.limpiar_escena()
ancho = 12.0
fondo = 8.0
alto_piso = 3.0
grosor_muro = 0.25
voladizo = 0.5
altura_cumbrera = 2.0
angulo_cumbrera = 10.0
A.crear_habitacion(nombre='Casa', ancho=ancho, fondo=fondo, alto=alto_piso + altura_cumbrera, grosor_muro=grosor_muro, material_muro='Muro_Pintura_Gris', material_suelo='Concreto_Piso', material_techo='Teja')
A.crear_techo_plano(nombre='TechoCumbrera', ancho=ancho, fondo=fondo, espesor=0.15, caida_x=0.0, caida_y=0.0, origen=(0, 0, alto_piso), material='Teja')