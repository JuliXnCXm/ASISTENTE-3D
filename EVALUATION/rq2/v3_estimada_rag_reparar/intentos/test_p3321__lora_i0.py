import blender_arch as A

A.limpiar_escena()

# 1. Crear la base de la terraza
terreno = A.crear_terreno_plano('BaseTerraza', ancho=20.0, fondo=15.0, espesor=0.3, origen=(0, 0, 0), material='Concreto_Piso')
techo_terraza = A.crear_techo_plano('TechoPlano', ancho=6.0, fondo=4.0, espesor=0.2, caida_x=0.0, caida_y=0.0, origen=(0, 0, 3.0), material='Parquet')

# 2. Crear mobiliario de la zona ajardinada
# Suelo de deck
suelo_deck = A.crear_terreno_plano('Deck', ancho=6.0, fondo=4.0, espesor=0.15, origen=(0, 0, 0.2), material='Madera_Deck')

# Jardineras de hormigón
for i in range(4):
    x_pos = -1.5 + i * 1.5
    A.crear_columna(f'ColumnaJardinera_{i}', seccion='circ', diametro=0.4, alto=0.4, origen=(x_pos, -1.5, 0.2), material='Hormigon')
    A.crear_columna(f'ColumnaJardinera_{i}', seccion='circ', diametro=0.4, alto=0.4, origen=(-1.5, x_pos, 0.2), material='Hormigon')
    A.crear_columna(f'ColumnaJardinera_{i}', seccion='circ', diametro=0.4, alto=0.4, origen=(1.5, x_pos, 0.2), material='Hormigon')
    A.crear_columna(f'ColumnaJardinera_{i}', seccion='circ', diametro=0.4, alto=0.4, origen=(-x_pos, 1.5, 0.2), material='Hormigon')

# Vegetación
for i in range(10):
    x_pos = -1.5 + i * 1.5
    y_pos = -1.5
    A.crear_arbol_simple(f'Arbol_{i}', radio_copa=0.3, altura_copa=1.2, altura_tronco=0.8, origen=(x_pos, y_pos, 0.2))

# 3. Crear la pérgola de acero
A.crear_columna('P_P1', seccion='rect', ancho=0.1, fondo=0.1, alto=2.8, origen=(-1.5, -1.5, 0.2), material='Acero_Inox')
A.crear_columna('P_P2', seccion='rect', ancho=0.1, fondo=0.1, alto=2.8, origen=(1.5, -1.5, 0.2), material='Acero_Inox')
A.crear_columna('P_P3', seccion='rect', ancho=0.1, fondo=0.1, alto=2.8, origen=(-1.5, 1.5, 0.2), material='Acero_Inox')
A.crear_columna('P_P4', seccion='rect', ancho=0.1, fondo=0.1, alto=2.8, origen=(1.5, 1.5, 0.2), material='Acero_Inox')

# Vigas principales
A.crear_losa_rectangular('Viga1', ancho=6.0, fondo=0.1, espesor=0.2, origen=(-3, -1.5, 2.8), material='Acero_Inox')
A.crear_losa_rectangular('Viga2', ancho=6.0, fondo=0.1, espesor=0.2, origen=(-3, 1.5, 2.8), material='Acero_Inox')

# Travesaños
for i in range(7):
    z_pos = 2.8 + i * 0.3
    A.crear_losa_rectangular(f'Travesano_{i}', ancho=0.1, fondo=4.0, espesor=0.1, origen=(-3, 0, z_pos), material='Acero_Inox')

# 4. Mobiliario de la zona de estar
sofa = A.crear_sofa('SofaTerraza', ancho=2.0, fondo=0.9, alto_asiento=0.45, alto_respaldo=0.85, origen=(0, 0, 0.2), material='Tela_Beige')
mesa = A.crear_mesa('MesaTerraza', ancho=1.2, fondo=0.6, alto=0.45, origen=(0, 1.5, 0.2), material_tablero='Madera_Roble')

# 5. Iluminación y cámara
A.agregar_luz('LuzPrincipal', tipo='AREA', ubicacion=(0, 0, 4.0), energia=200)
A.crear_camara('CamaraTerraza', ubicacion=(10, -10, 8), rotacion=(70, 0, 45), activa=True)