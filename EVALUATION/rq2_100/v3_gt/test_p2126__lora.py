import blender_arch as A
A.limpiar_escena()

# 1. Crear la base del deck
deck = A.crear_piso('Deck', ancho=7, fondo=5, espesor=0.15, material='Madera_Roble')

# 2. Crear soportes de la pérgola
soportes = []
for i in [-3, 3]:
    for j in [-2, 2]:
        loc_x = i * 3.5
        loc_y = j * 2.5
        soporte = A.crear_columna(f'Soporte_{i}_{j}', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(loc_x, loc_y, 0), material='Madera_Roble')
        soportes.append(soporte)

# 3. Crear vigas principales de la pérgola
viga1 = A.crear_losa_rectangular('Viga_Principal_1', ancho=7, fondo=0.15, espesor=0.2, origen=(-3.5, -2.5, 2.8), material='Madera_Roble')
viga2 = A.crear_losa_rectangular('Viga_Principal_2', ancho=7, fondo=0.15, espesor=0.2, origen=(3.5, 2.5, 2.8), material='Madera_Roble')

# 4. Crear listones de techo
num_listones = 12
espacio_liston = 0.1
for i in range(num_listones):
    pos_x = -3.5 + i * (7 / num_listones)
    A.crear_losa_rectangular(f'Liston_{i}', ancho=0.1, fondo=0.15, espesor=0.1, origen=(pos_x, -2.5, 2.8 + 0.2), material='Madera_Roble')

# 5. Crear maceteros de hormigón
macetero1 = A.crear_conejo('Macetero_1', radio_base=1.2, altura_base=0.4, altura_copa=0.8, origen=(-4, -3, 0), material='Hormigon')
macetero2 = A.crear_conejo('Macetero_2', radio_base=1.2, altura_base=0.4, altura_copa=0.8, origen=(4, 3, 0), material='Hormigon')

# 6. Añadir vegetación
A.crear_arbol_simple('Arbol_1', radio_copa=1.0, altura_copa=2.0, altura_tronco=1.2, origen=(-4, -2, 0))
A.crear_arbol_simple('Arbol_2', radio_copa=1.0, altura_copa=2.0, altura_tronco=1.2, origen=(4, 2, 0))