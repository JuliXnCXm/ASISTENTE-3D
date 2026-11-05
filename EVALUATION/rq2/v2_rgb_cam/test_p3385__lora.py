import blender_arch as A
A.limpiar_escena()

# --- ESTRUCTURA Y MUEBLES BASE ---
A.crear_habitacion('Sala', ancho=5.2, fondo=4.0, alto=2.8, material_muro='Estuco', material_suelo='Porcelanato')
A.crear_habitacion('Dormitorio', ancho=4.0, fondo=4.0, alto=2.8, origen=(0, 5.2, 0), material_muro='Estuco', material_suelo='Parquet')
A.crear_pared('Muro_Pasillo', largo=5.2, alto=2.8, origen=(0, 9.2, 0), material='Estuco')
A.crear_pared('Muro_Cocina', largo=4.0, alto=2.8, origen=(9.2, 0, 0), material='Estuco')
A.crear_pared('Muro_Bano', largo=4.0, alto=2.8, origen=(9.2, 4.0, 0), material='Estuco')
A.crear_pared('Muro_Ventana_Dorm', largo=4.0, alto=1.8, origen=(0, 5.2, 0), rotacion_z=90)
A.crear_pared('Muro_Ventana_Sala', largo=5.2, alto=1.8, origen=(0, 0, 0), rotacion_z=90)

# --- MOBILIARIO ---
A.crear_sofa('Sofa', ancho=2.2, fondo=0.9, origen=(1.5, 3.0, 0), material='Tela_Gris')
A.crear_mesa('Mesa_Nuevo', ancho=1.2, fondo=0.6, alto=0.75, origen=(2.0, 1.5, 0), material_tablero='Madera_Roble')
A.crear_armario('Armario_Dorm', ancho=2.5, alto=2.4, fondo=0.6, origen=(3.5, 0.2, 0), material_cuerpo='MDF_Blanco')
A.crear_barra('Barra_Cocina', ancho=1.8, alto=0.9, origen=(9.2 + 0.2, 2.0, 0), material_tablero='Acero_Inox')

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('Luz_Sala', tipo='AREA', ubicacion=(2.6, 2.0, 2.7), energia=250)
A.agregar_luz('Luz_Dorm', tipo='AREA', ubicacion=(3.0, 2.0, 2.7), energia=250)
A.crear_camara('Camara_Principal', ubicacion=(-5, -5, 5), rotacion=(70, 0, -45), activa=True)