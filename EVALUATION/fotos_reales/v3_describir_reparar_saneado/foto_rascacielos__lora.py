import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Rascacielos_Corporativo', pisos=45, ancho=100.0, fondo=50.0, alto_piso=3.6, grosor_muro=0.25, grosor_losa=0.3, con_techo_plano=True, con_columnas=True, seccion_columna='rect', dim_columna=0.4, modulo_columna_x=10.0, modulo_columna_y=10.0, ventanas_fachada=True, ventana_ancho=2.0, ventana_alto=2.2, ventana_alfeizar=0.2, ventana_separacion=5.0, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon', material_vidrio='Vidrio_Templado', material_marco='Marco_Aluminio', material_columna='Hormigon_Visto', origen=(0, 0, 0))
for i in range(2):
    A.crear_losa_rectangular(f'Balcon_{i}', ancho=10.0, fondo=1.5, espesor=0.2, origen=(-5 + i * 2, 5, 44.8), material='Hormigon')
for i in range(5):
    A.crear_losa_rectangular(f'Balcon_{i}', ancho=10.0, fondo=1.5, espesor=0.2, origen=(-5 + i * 2, 5, 44.8), material='Hormigon')