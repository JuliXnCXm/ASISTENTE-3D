import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=4, ancho=12, fondo=14, alto_piso=3, origen=(0, 0, 0))
A.crear_losa_rectangular('Balcon_1', ancho=3, fondo=1.5, espesor=0.2, origen=(4.5, 14, 3))
A.crear_baranda_lineal('Balcon_1_Baranda', largo=3, altura=1.1, origen=(4.5, 15.42, 3.2))
A.crear_losa_rectangular('Balcon_2', ancho=3, fondo=1.5, espesor=0.2, origen=(4.5, 14, 6))
A.crear_baranda_lineal('Balcon_2_Baranda', largo=3, altura=1.1, origen=(4.5, 15.42, 6.2))
A.crear_losa_rectangular('Balcon_3', ancho=3, fondo=1.5, espesor=0.2, origen=(4.5, 14, 9))
A.crear_baranda_lineal('Balcon_3_Baranda', largo=3, altura=1.1, origen=(4.5, 15.42, 9.2))
