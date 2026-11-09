import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=3, ancho=20, fondo=10, alto_piso=3, origen=(0, 0, 0))
A.crear_losa_rectangular('Marquesina', ancho=1.5, fondo=4, espesor=0.15, origen=(-1.5, 3, 3))
