import blender_arch as A
A.limpiar_escena()
A.crear_edificio_n_pisos(nombre='Fachada_Edificio', pisos=3, ancho=15.0, fondo=0.2, alto_piso=3.2, grosor_muro=0.2, con_techo_plano=False, ventanas_fachada=True, ventana_ancho=1.5, ventana_alto=1.8, ventana_alfeizar=0.9, ventana_separacion=3.0, material_fachada='Ladrillo', material_marco='Marco_Negro', material_vidrio='Vidrio_Templado')