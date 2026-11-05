import blender_arch as A
A.limpiar_escena()
hab = A.crear_habitacion(nombre='Oficina', ancho=4.0, fondo=3.0, alto=2.8, material_muro='Muro_Pintura_Gris', material_suelo='Parquet')
A.crear_mesa(nombre='Escritorio_L', ancho=1.8, fondo=0.9, alto=0.75, origen=(1.6, 1.5, 0), material_tablero='Madera_Roble')
A.crear_silla(nombre='Silla_Oficina', origen=(1.6, 0.6, 0), material='Cuero')
pos_estanteria = (2.0, 0.2, 0)
for i in range(4):
    A.crear_caja(f'Caja_Estanteria_{i}', ancho=0.3, fondo=0.3, alto=0.8, origen=(pos_estanteria[0], pos_estanteria[1], pos_estanteria[2]), material='MDF_Blanco')
    pos_estanteria = (pos_estanteria[0] + 0.3, pos_estanteria[1], pos_estanteria[2])