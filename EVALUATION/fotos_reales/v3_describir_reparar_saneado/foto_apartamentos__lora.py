import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Centro', pisos=4, ancho=20.0, fondo=15.0, alto_piso=3.2, grosor_muro=0.25, grosor_losa=0.3, con_techo_plano=True, con_columnas=False, ventanas_fachada=True, ventana_ancho=1.5, ventana_alto=1.8, ventana_alfeizar=1.0, origen=(0, 0, 0), material_fachada='Muro_Pintura_Rosa', material_losa='Hormigon', material_vidrio='Vidrio_Templado', material_marco='Marco_Aluminio')
A.crear_piso(nombre='Garaje', ancho=20.0, fondo=15.0, espesor=0.5, origen=(0, 0, -0.5), material='Concreto_Piso')