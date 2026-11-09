import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=20, fondo=12, alto_piso=3, origen=(0, 0, 0))
A.crear_losa_rectangular('Balcon', ancho=3, fondo=1.5, espesor=0.2, origen=(8.5, 12, 3))
A.crear_baranda_lineal('Balcon_Baranda', largo=3, altura=1.1, origen=(8.5, 13.42, 3.2))
