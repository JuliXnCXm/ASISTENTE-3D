import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Civil', pisos=3, ancho=12.0, fondo=14.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_muro='Muro_Pintura_Gris', material_losa='Hormigon')
alto_edificio_base = 3 * 3.0
ancho_atico = 5.0
fondo_atico = 3.0
alto_atico = 3.0
pos_x_atico = (12.0 - ancho_atico) / 2
pos_y_atico = (14.0 - fondo_atico) / 2
A.crear_habitacion(nombre='Atico', ancho=ancho_atico, fondo=fondo_atico, alto=alto_atico, origen=(pos_x_atico, pos_y_atico, alto_edificio_base), material_muro='Muro_Pintura_Gris')