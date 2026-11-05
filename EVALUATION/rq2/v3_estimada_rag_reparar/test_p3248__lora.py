import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Apartamentos', pisos=4, ancho=15.0, fondo=15.0, alto_piso=2.8, grosor_muro=0.2, grosor_losa=0.2, con_techo_plano=True, con_columnas=False, seccion_columna='rect', dim_columna=(0, 0), modulo_columna_x=4.0, modulo_columna_y=5.0, ventanas_fachada=True, ventana_ancho=1.2, ventana_alto=1.1, ventana_alfeizar=0.9, ventana_separacion=2.4, origen=(0, 0, 0), material_muro='Muro_Pintura', material_losa='Hormigon', material_fachada='Muro_Pintura_Gris', material_vidrio='Vidrio_Templado', material_marco='Marco_Aluminio', material_columna='Hormigon')
techo_plano = A.crear_techo_plano(nombre='Terraza', ancho=15.0, fondo=15.0, espesor=0.2, caida_x=0.0, caida_y=0.0, origen=(0, 0, 2.8 + 0.2), material='Concreto_Piso')
for i in range(4):
    pos_x = -7.5 + i * 4
    A.crear_muro(f'Jardinera_{i}', largo=4.0, alto=0.8, grosor=0.2, origen=(pos_x, -7.5, 2.8 + 0.2), material='Hormigon')
    A.crear_muro(f'Jardinera_{i}_Frontal', largo=4.0, alto=0.8, grosor=0.2, origen=(-7.5, pos_x, 2.8 + 0.2), material='Hormigon')
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(5, -10, 10), energia=2.5)
A.crear_camara('Camara_Fachada', ubicacion=(10, -12, 6), rotacion=(70, 0, 0))