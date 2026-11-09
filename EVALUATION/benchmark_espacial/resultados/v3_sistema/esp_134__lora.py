import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=4, ancho=16, fondo=12, alto_piso=3, origen=(0, 0, 0))
volumen_cubierta = A.crear_losa_rectangular('Volumen_Cubierta', ancho=4.0, fondo=3.0, espesor=3.0, origen=(8.0, 6.0, 12.0))