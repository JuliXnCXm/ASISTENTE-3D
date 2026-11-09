import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=20, fondo=10, alto_piso=3, origen=(0, 0, 0))
ed2 = A.crear_edificio_n_pisos('Edificio2', pisos=1, ancho=8, fondo=6, alto_piso=3, origen=(-13, 2, 0))
