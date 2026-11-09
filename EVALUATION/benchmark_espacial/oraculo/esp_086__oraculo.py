import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=3, ancho=18, fondo=10, alto_piso=3, origen=(0, 0, 0))
ed2 = A.crear_edificio_n_pisos('Edificio2', pisos=1, ancho=6, fondo=7, alto_piso=3, origen=(6, -13, 0))
