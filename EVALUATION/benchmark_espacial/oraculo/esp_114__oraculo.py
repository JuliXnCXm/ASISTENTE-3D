import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
bx = A.crear_edificio_n_pisos('BrazoX', pisos=2, ancho=20, fondo=6, alto_piso=3, origen=(0, 0, 0))
by = A.crear_edificio_n_pisos('BrazoY', pisos=2, ancho=7, fondo=8, alto_piso=3, origen=(13, 6, 0))
