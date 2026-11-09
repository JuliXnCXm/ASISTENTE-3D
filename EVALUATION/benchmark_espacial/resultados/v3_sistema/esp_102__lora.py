import blender_arch as A
A.limpiar_escena()
ancho = 8.0
fondo = 10.0
alto_piso = 3.0
grosor_muro = 0.25
altura_cumbrera = 2.0
angulo_cumbrera = 10.0
volumen_casa = A.crear_habitacion(nombre='Casa', ancho=ancho, fondo=fondo, alto=alto_piso, grosor_muro=grosor_muro, material_muro='Muro_Pintura_Gris', material_suelo='Porcelanato')
A.crear_techo_plano(nombre='TechoCumbrera', ancho=ancho, fondo=fondo, espesor=0.15, caida_x=0.0, caida_y=0.0, origen=(0, 0, alto_piso), material='Teja')
A.rotar_objecto(volumen_casa, angulo_cumbrera, 'Y')