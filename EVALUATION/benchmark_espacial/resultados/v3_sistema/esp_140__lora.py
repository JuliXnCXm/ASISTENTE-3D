import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=3, ancho=18, fondo=14, alto_piso=3, origen=(0, 0, 0))
ed2 = A.crear_edificio_n_pisos('Edificio_Nuevo', pisos=2, ancho=8, fondo=6, alto_piso=3, origen=(-10, -5, 0))