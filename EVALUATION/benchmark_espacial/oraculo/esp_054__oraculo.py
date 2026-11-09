import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=16, fondo=10, alto_piso=3, origen=(0, 0, 0))
A.crear_losa_rectangular('Balcon_1', ancho=3, fondo=1.5, espesor=0.2, origen=(6.5, 10, 3))
A.crear_baranda_lineal('Balcon_1_Baranda', largo=3, altura=1.1, origen=(6.5, 11.42, 3.2))
A.crear_losa_rectangular('Balcon_2', ancho=3, fondo=1.5, espesor=0.2, origen=(6.5, 10, 6))
A.crear_baranda_lineal('Balcon_2_Baranda', largo=3, altura=1.1, origen=(6.5, 11.42, 6.2))
A.crear_losa_rectangular('Balcon_3', ancho=3, fondo=1.5, espesor=0.2, origen=(6.5, 10, 9))
A.crear_baranda_lineal('Balcon_3_Baranda', largo=3, altura=1.1, origen=(6.5, 11.42, 9.2))
A.crear_losa_rectangular('Balcon_4', ancho=3, fondo=1.5, espesor=0.2, origen=(6.5, 10, 12))
A.crear_baranda_lineal('Balcon_4_Baranda', largo=3, altura=1.1, origen=(6.5, 11.42, 12.2))
A.crear_losa_rectangular('Balcon_5', ancho=3, fondo=1.5, espesor=0.2, origen=(6.5, 10, 15))
A.crear_baranda_lineal('Balcon_5_Baranda', largo=3, altura=1.1, origen=(6.5, 11.42, 15.2))
