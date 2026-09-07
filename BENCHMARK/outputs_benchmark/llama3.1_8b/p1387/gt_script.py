import blender_arch as A
A.limpiar_escena()
grosor_muro = 0.25
muro_frente = A.crear_muro('FachadaPrincipal', largo=10, alto=6, grosor=grosor_muro, material='Ladrillo_Rojo')

# Origen de la puerta para que quede centrada en el muro
puerta_ancho = 1.2
puerta_x_origen = 10/2 - puerta_ancho/2
A.crear_puerta('PuertaEntrada', ancho=puerta_ancho, alto=2.2, prof_marco=grosor_muro, origen=(puerta_x_origen, -grosor_muro/2, 0), material_panel='Madera_Roble', material_marco='Marco_Negro')

# Colocar ventanas simétricamente en los espacios restantes
ventana_ancho = 1.5
espacio_lateral = puerta_x_origen
ventana_x_izq = espacio_lateral / 2 - ventana_ancho / 2
ventana_x_der = 10 - espacio_lateral / 2 - ventana_ancho / 2
A.crear_ventana('VentanaIzq', ancho=ventana_ancho, alto=1.1, prof_marco=grosor_muro, origen=(ventana_x_izq, -grosor_muro/2, 1.0), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.crear_ventana('VentanaDer', ancho=ventana_ancho, alto=1.1, prof_marco=grosor_muro, origen=(ventana_x_der, -grosor_muro/2, 1.0), material_marco='Marco_Negro', material_vidrio='Vidrio')