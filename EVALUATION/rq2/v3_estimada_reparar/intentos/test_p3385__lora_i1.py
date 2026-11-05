import blender_arch as A
A.limpiar_escena()
ancho_total = 6.0
fondo_total = 9.0
alto_piso = 2.8
A.crear_habitacion(nombre='SalaComedor', ancho=4.0, fondo=5.0, alto=alto_piso, material_muro='Muro_Pintura_Gris', material_suelo='Parquet')
A.crear_habitacion(nombre='Dormitorio', ancho=2.0, fondo=4.0, alto=alto_piso, origen=(2.0, 5.0, 0), material_muro='Muro_Pintura_Gris', material_suelo='Parquet')
A.crear_habitacion(nombre='Cocina', ancho=2.0, fondo=2.5, alto=alto_piso, origen=(4.0, 2.5, 0), material_muro='Muro_Pintura_Gris', material_suelo='Porcelanato')
A.crear_habitacion(nombre='BarraCocina', ancho=1.2, fondo=0.6, alto=alto_piso, origen=(5.2, 2.5, 0), material_muro='Muro_Pintura_Gris', material_suelo='Porcelanato')
A.crear_habitacion(nombre='PasilloAcceso', ancho=1.0, fondo=1.5, alto=alto_piso, origen=(4.0, 0.5, 0), material_muro='Muro_Pintura_Gris', material_suelo='Parquet')
A.crear_habitacion(nombre='Baño', ancho=2.0, fondo=1.5, alto=alto_piso, origen=(4.0, 6.5, 0), material_muro='Muro_Pintura_Gris', material_suelo='Porcelanato')
A.crear_armario(nombre='ArmarioDormitorio', ancho=2.0, alto=2.4, fondo=0.6, origen=(2.0, 3.5, 0), material_cuerpo='MDF_Blanco')
A.crear_mesa(nombre='MesaComedor', ancho=1.4, fondo=0.8, alto=0.75, origen=(2.0, 3.0, 0), material_tablero='Madera_Roble')
A.crear_sofa(nombre='SofaSala', ancho=2.2, fondo=0.9, origen=(4.0, 3.0, 0), material='Tela_Gris')
A.crear_ventana(nombre='VentanaSala', ancho=2.0, alto=1.2, prof_marco=0.2, origen=(4.0, 0.5, 1.0), material_marco='Marco_Aluminio', material_vidrio='Vidrio')
A.crear_ventana(nombre='VentanaDormitorio', ancho=1.5, alto=1.2, prof_marco=0.2, origen=(2.0, 5.0, 1.0), material_marco='Marco_Aluminio', material_vidrio='Vidrio')
A.crear_ventana(nombre='VentanaCocina', ancho=1.5, alto=1.2, prof_marco=0.2, origen=(4.0, 2.5, 1.0), material_marco='Marco_Aluminio', material_vidrio='Vidrio')