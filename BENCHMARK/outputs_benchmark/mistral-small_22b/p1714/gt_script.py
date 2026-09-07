import blender_arch as A

A.limpiar_escena()
muro_frontal = A.crear_muro('MuroPerimetral', largo=10, alto=2.5, grosor=0.2, origen=(-5, 0, 0), material='Ladrillo_Rojo')
A.crear_puerta('PuertaEntrada', ancho=1.5, alto=2.2, prof_marco=0.2, origen=(-0.75, 0, 0), material_panel='Madera_Roble', material_marco='Marco_Negro')
A.abrir_vanos_batch_rectangulares(muro_frontal, centros_world=[(0, 0, 1.1)], ancho=1.5, alto=2.2)