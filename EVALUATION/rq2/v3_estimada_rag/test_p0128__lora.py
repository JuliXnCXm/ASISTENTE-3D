import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la estantería
ancho_total = 0.8
profundidad_total = 0.3
alto_total = 1.8
num_estantes = 5
grosor_panel = 0.02

ancho_estante = ancho_total / num_estantes
alto_estante = alto_total / num_estantes

for i in range(num_estantes):
    pos_x = -ancho_total / 2 + ancho_estante / 2 + i * ancho_estante
    pos_z = i * alto_estante
    
    A.crear_losa_rectangular(f'Estante_{i+1}', ancho=ancho_estante, fondo=profundidad_total, espesor=grosor_panel, origen=(pos_x, 0, pos_z), material='Madera_Roble')

# Crear soportes verticales
for i in range(num_estantes + 1):
    pos_x = -ancho_total / 2 + ancho_estante / 2 + i * ancho_estante
    A.crear_losa_rectangular(f'Soporte_{i}', ancho=grosor_panel, fondo=profundidad_total, espesor=alto_total, origen=(pos_x, 0, 0), material='Madera_Roble')