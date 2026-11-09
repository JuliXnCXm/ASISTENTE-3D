import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
bx = A.crear_edificio_n_pisos('BrazoX', pisos=3, ancho=18, fondo=6, alto_piso=3, origen=(0, 0, 0))
by = A.crear_edificio_n_pisos('BrazoY', pisos=3, ancho=6, fondo=8, alto_piso=3, origen=(12, 6, 0))
