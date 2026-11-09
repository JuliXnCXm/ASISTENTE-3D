import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=20, fondo=12, alto_piso=3, origen=(0, 0, 0))
A.crear_volumen_rectangular('Volumen_Cubierta', ancho=4.0, fondo=4.0, alto=3.0, origen=(0, 0, 6.0), material='Hormigon')