import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=3, ancho=18, fondo=12, alto_piso=3, origen=(0, 0, 0))
A.crear_losa_rectangular('Balcon_1', ancho=1.5, fondo=3, espesor=0.2, origen=(-1.5, 4.5, 3))
_b = A.crear_baranda_lineal('Balcon_1_Baranda', largo=3, altura=1.1, origen=(-1.42, 4.5, 3.2))
_b.rotation_euler.z = math.pi / 2
A.crear_losa_rectangular('Balcon_2', ancho=1.5, fondo=3, espesor=0.2, origen=(-1.5, 4.5, 6))
_b = A.crear_baranda_lineal('Balcon_2_Baranda', largo=3, altura=1.1, origen=(-1.42, 4.5, 6.2))
_b.rotation_euler.z = math.pi / 2
