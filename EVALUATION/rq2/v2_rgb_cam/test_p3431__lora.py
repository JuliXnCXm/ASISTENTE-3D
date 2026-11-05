import blender_arch as A
A.limpiar_escena()

# Crear la estructura de la cocina en L
hab = A.crear_habitacion('Cocina', ancho=5, fondo=4, alto=2.8, material_muro='Muro_Pintura_Gris', material_suelo='Porcelanato')

# Módulos bajos y altos
A.crear_armario('Mod_Bajo_1', ancho=2.5, alto=0.9, fondo=0.6, num_puertas=2, origen=(0, 0.2, 0), material_cuerpo='MDF_Blanco')
A.crear_armario('Mod_Bajo_2', ancho=2.5, alto=0.9, fondo=0.6, num_puertas=2, origen=(2.5, 0.2, 0), material_cuerpo='MDF_Blanco')
A.crear_encimera('Encimera', ancho=5, fondo=0.6, espesor=0.04, origen=(0, 0.2, 0.9), material='Cuarzo_Blanco')

# Isla central
A.crear_mesa('Isla_Central', ancho=2.0, fondo=1.0, alto=0.9, origen=(1.5, 3.0, 0), material_tablero='Madera_Nogal')
A.crear_silla('Taburete_Isla_1', origen=(1.5, 2.5, 0), material='Acero_Inox')
A.crear_silla('Taburete_Isla_2', origen=(2.5, 2.5, 0), material='Acero_Inox')

# Ventilador de cocina
A.crear_ventilador('Extractor', ancho=0.9, alto=0.2, prof=0.1, origen=(2.5, 0.2, 2.4), material_caja='Acero_Inox', material_aspa='Acero_Inox')