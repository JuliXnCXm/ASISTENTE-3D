import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=10, fondo=14, alto_piso=3, origen=(0, 0, 0))
ancho_fachada = ed.dimensions[0]
fondo_fachada = ed.dimensions[2]
alto_piso = ed.pisos[2].dimensions[2]
origen_balcon = (0, -fondo_fachada / 2 + 1.5 / 2, alto_piso * 2.5)
A.crear_losa_rectangular('Balcon_Trasero', ancho=3.0, fondo=1.5, espesor=0.2, origen=origen_balcon, material='Hormigon')
A.crear_baranda_lineal('Baranda_Balcon', largo=3.0, origen=(origen_balcon[0], origen_balcon[1] - 1.5 / 2, alto_piso * 2.5), material='Acero_Inox')