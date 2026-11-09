import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=4, ancho=16, fondo=12, alto_piso=3, origen=(0, 0, 0))
ed2 = A.crear_edificio_n_pisos('Edificio2', pisos=1, ancho=9, fondo=7, alto_piso=3, origen=(3.5, -17, 0))
