import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
bx = A.crear_edificio_n_pisos('BrazoX', pisos=4, ancho=18, fondo=6, alto_piso=3, origen=(0, 10, 0))
by = A.crear_edificio_n_pisos('BrazoY', pisos=4, ancho=6, fondo=10, alto_piso=3, origen=(0, 0, 0))
