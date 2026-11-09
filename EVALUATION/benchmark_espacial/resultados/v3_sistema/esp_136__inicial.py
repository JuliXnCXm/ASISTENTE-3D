import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=20, fondo=14, alto_piso=3, origen=(0, 0, 0))
ancho_balcon = 3.0
fondo_balcon = 1.5
alto_baranda = 1.0
origen_balcon = (0, -fondo_balcon / 2, 9.0)
A.crear_losa_rectangular('Balcon_Izq', ancho=ancho_balcon, fondo=fondo_balcon, espesor=0.2, origen=origen_balcon, material='Hormigon')
A.crear_baranda_lineal('Baranda_Izq', largo=ancho_balcon, origen=(origen_balcon[0], origen_balcon[1] + fondo_balcon / 2, 9.0), material='Acero_Inox')