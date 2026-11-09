import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=16, fondo=14, alto_piso=3, origen=(0, 0, 0))
volumen_cubierta = A.crear_volumen('Volumen_Cubierta', ancho=4.0, fondo=3.0, alto=3.0, origen=(8.0, 7.0, 9.0), material='Hormigon')