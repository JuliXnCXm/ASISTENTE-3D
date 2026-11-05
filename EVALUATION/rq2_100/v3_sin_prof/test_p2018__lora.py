import blender_arch as A
import bpy

A.limpiar_escena()

# Muro de soporte
muro = A.crear_muro('MuroEscalera', largo=2.5, alto=2.8, grosor=0.15, origen=(0,0,-0.1), material='Muro_Pintura_Gris')

# Peldanos de madera flotantes
for i in range(16):
    x = 0.1 + i * 0.25
    z = 0.15 + i * 0.25
    A.crear_losa_rectangular(f'Peldano_{i}', ancho=0.18, fondo=0.3, espesor=0.05, origen=(x, 0, z), material='Madera_Roble')

# Baranda de vidrio
panel_vigas = A.crear_losa_rectangular('PanelBaranda', ancho=2.5, fondo=0.1, espesor=0.02, origen=(-1.25, 0, 2.7), material='Vidrio_Templado')
panel_barandas = A.crear_losa_rectangular('PanelBarandas', ancho=2.5, fondo=0.02, espesor=0.1, origen=(-1.25, 0, 2.75), material='Marco_Negro')

# Pasamanos metálico
A.crear_baranda_lineal('Pasamanos', largo=2.5, origen=(-1.25, 0, 2.75), material='Acero_Inox')