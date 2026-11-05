import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y SUELO ---
A.crear_losa_rectangular('Losa_Terraza', ancho=12, fondo=6, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')
A.crear_piso('Deck_Madera', ancho=12, fondo=6, espesor=0.05, origen=(0,0,0.2), material='Madera_Roble')

# --- JARDINERÍAS PERIMETRALES ---
for i in range(4):
    x = -5 + i * 3
    A.crear_losa_rectangular(f'Jardinera_{i}', ancho=1.5, fondo=0.5, espesor=0.4, origen=(x, -2.5, 0.2), material='Hormigon')
    A.crear_planta_simple(f'Vegetacion_{i}', radio_copa=0.7, altura_copa=1.2, altura_tronco=0.5, origen=(x, -2.5, 0.6))

# --- PÉRGOLA DE ACERO ---
A.crear_techo_plano('Techo_Pergola', ancho=10, fondo=4, espesor=0.2, origen=(-5, 2, 0.2), material='Acero_Inox')
A.crear_columna('Columna_Pergola_1', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(-5.1, 2.1, 0.2), material='Acero_Inox')
A.crear_columna('Columna_Pergola_2', seccion='rect', ancho=0.2, fondo=0.2, alto=2.5, origen=(5.1, 2.1, 0.2), material='Acero_Inox')

# --- ZONA DE ESTAR CON BLNDER ---
# Sofá
bpy.ops.mesh.primitive_cube_add(location=(-2, -1, 0.2))
sofa = bpy.context.active_object
sofa.name = 'Sofa'
sofa.dimensions = (2.0, 0.9, 0.05)
A.asignar_material(sofa, nombre='Cuero', base_color=(0.8, 0.6, 0.4, 1))

# Mesa
bpy.ops.mesh.primitive_cube_add(location=(-2, 0, 0.2))
mesa = bpy.context.active_object
mesa.name = 'Mesa'
mesa.dimensions = (1.2, 0.6, 0.05)
A.asignar_material(mesa, nombre='Madera_Nogal', base_color=(0.5, 0.3, 0.2, 1))