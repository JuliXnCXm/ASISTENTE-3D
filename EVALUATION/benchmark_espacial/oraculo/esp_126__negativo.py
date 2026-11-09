import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=4, ancho=16, fondo=8, alto_piso=3, origen=(0, 0, 0))
A.crear_losa_rectangular('Balcon', ancho=3, fondo=1.5, espesor=0.2, origen=(6.5, 8, 6))
A.crear_baranda_lineal('Balcon_Baranda', largo=3, altura=1.1, origen=(6.5, 9.42, 6.2))
