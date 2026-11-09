import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=5, ancho=18, fondo=8, alto_piso=3, origen=(0, 0, 0))
A.crear_losa_rectangular('Marquesina', ancho=4, fondo=1.5, espesor=0.15, origen=(7, -1.5, 3))
