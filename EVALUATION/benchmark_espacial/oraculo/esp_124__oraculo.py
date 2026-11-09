import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
v0 = A.crear_edificio_n_pisos('Volumen_1', pisos=3, ancho=20, fondo=20, alto_piso=3, origen=(0, 0, 0))
v0.location.z = 0
v1 = A.crear_edificio_n_pisos('Volumen_2', pisos=3, ancho=16, fondo=16, alto_piso=3, origen=(2, 2, 0))
v1.location.z = 9.2
v2 = A.crear_edificio_n_pisos('Volumen_3', pisos=3, ancho=12, fondo=12, alto_piso=3, origen=(4, 4, 0))
v2.location.z = 18.4
v3 = A.crear_edificio_n_pisos('Volumen_4', pisos=3, ancho=8, fondo=8, alto_piso=3, origen=(6, 6, 0))
v3.location.z = 27.6
