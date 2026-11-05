import blender_arch as A
A.limpiar_escena()
hab = A.crear_habitacion(nombre='Sala_Estar', ancho=4.0, fondo=5.0, alto=2.8, material_muro='Muro_Pintura_Gris', material_suelo='Parquet')
sofa = A.crear_sofa(nombre='Sofa_Principal', ancho=2.2, origen=(1.4, 0.2, 0), material='Tela_Beige')
alfombra = A.crear_piso(nombre='Alfombra_Sala', ancho=2.5, fondo=1.8, espesor=0.05, origen=(1.25, 2.0, 0), material='Textil_Blanco')
estanteria_modular = []
ancho_total = 1.2
separacion = 0.1
for i in range(4):
    x_pos = 0.1 + i * (ancho_total / 3)
    y_pos = 0.2 + separacion
    estanteria = A.crear_estanteria(nombre=f'Estanteria_{i + 1}', ancho=0.3, alto=2.2, fondo=0.3, num_estantes=5, origen=(x_pos, y_pos, 0), material='Madera_Roble')
    estanteria_modular.append(estanteria)