import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA ---
A.crear_habitacion('Sala', ancho=4.5, fondo=5.0, alto=2.8, material_muro='Muro_Pintura')
A.crear_habitacion('Comedor', ancho=3.0, fondo=4.0, alto=2.8, origen=(4.5, 0, 0), material_muro='Muro_Pintura')
A.crear_habitacion('Cocina', ancho=3.0, fondo=3.0, alto=2.8, origen=(7.5, 0, 0), material_muro='Muro_Pintura')
A.crear_habitacion('Baño', ancho=2.5, fondo=2.0, alto=2.8, origen=(0, 6.0, 0), material_muro='Muro_Pintura')

# --- MUEBLES ---
A.crear_mesa('Mesa_Comedor', ancho=1.8, fondo=0.9, alto=0.75, origen=(3.0, 3.5, 0), material_tablero='Madera_Roble')
A.crear_sofa('Sofa_Sala', ancho=2.5, fondo=0.9, origen=(1.5, 1.5, 0), material='Tela_Gris')
A.crear_armario('Armario_Cocina', ancho=2.0, alto=2.4, fondo=0.6, origen=(5.5, 0.2, 0), material_cuerpo='MDF_Blanco')

# --- ILUMINACION Y CAMARA ---
A.agregar_luz('Luz_Principal', tipo='AREA', ubicacion=(7.5, 2.5, 2.7), energia=800)
A.crear_camara('Camara', ubicacion=(7.5, -5, 2.5), rotacion=(75, 0, 0))