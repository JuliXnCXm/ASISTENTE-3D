import blender_arch as A
A.limpiar_escena()

# 1. Suelo de Terraza
suelo_terraza = A.crear_piso('Suelo_Terraza', ancho=10, fondo=8, espesor=0.15, material='Madera_Deck')

# 2. Pérgola de Acero
A.crear_techo_plano('Pergola_Cubierta', ancho=8, fondo=6, espesor=0.2, origen=(1, 1, 0.15), material='Acero_Inox')
postes = [(1.5, 1.5, 0.15), (8.5, 1.5, 0.15), (1.5, 6.5, 0.15), (8.5, 6.5, 0.15)]
for i, p in enumerate(postes):
    A.crear_columna(f'Poste_{i}', seccion='rect', ancho=0.1, fondo=0.1, alto=0.2, origen=p, material='Acero_Inox')
    A.crear_barra(f'Viga_Horizontal_{i}', largo=8, origen=(p[0], 1.5, 0.2), material='Acero_Inox')
    A.crear_barra(f'Viga_Vertical_{i}', largo=6, origen=(1.5, p[1], 0.2), material='Acero_Inox')

# 3. Jardineras Perimetrales
for i in range(4):
    A.crear_hormigon(f'Jardinera_{i}', ancho=2.5, fondo=0.5, alto=0.4, origen=(1 + 2.5*i, 1, 0.15), material='Hormigon')
    A.crear_planta(f'Vegetacion_{i}', nombre=f'Planta_{i}', origen=(1 + 2.5*i, 1.25, 0.2))

# 4. Iluminación y Cámara
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(-10, -10, 15), energia=2.5)
A.crear_camara('Camara_Terraza', ubicacion=(10, -10, 8), rotacion=(70, 0, 45))