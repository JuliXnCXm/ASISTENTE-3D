import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=5, ancho=12, fondo=12, alto_piso=3, origen=(0, 0, 0))
ed2 = A.crear_edificio_n_pisos('Edificio2', pisos=2, ancho=9, fondo=6, alto_piso=3, origen=(1.5, 32, 0))
