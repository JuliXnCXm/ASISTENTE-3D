import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=4, ancho=12, fondo=8, alto_piso=3, origen=(0, 0, 0))
ancho_balcon = 3.0
profundidad_balcon = 1.5
alto_baranda = 1.0
origen_balcon = (0, -profundidad_balcon / 2, 3.0)
A.crear_losa_rectangular('LosaBalcon', ancho=ancho_balcon, fondo=profundidad_balcon, espesor=0.2, origen=origen_balcon, material='Hormigon')
A.crear_baranda_lineal('BarandaBalcon', largo=ancho_balcon, origen=(origen_balcon[0], origen_balcon[1] + profundidad_balcon / 2, 3.0), material='Acero_Inox')