import blender_arch as A

A.limpiar_escena()
A.crear_piso('PisoPatio', ancho=5.0, fondo=4.0, espesor=0.1, material='Concreto_Piso')
A.crear_muro('MuroFondo', largo=5.0, alto=2.5, origen=(0, 4.0, 0), material='Ladrillo_Rojo')