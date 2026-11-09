import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=5, ancho=14, fondo=8, alto_piso=3, origen=(0, 0, 0))
A.crear_losa_rectangular('Volumen_Cubierta', ancho=4.0, fondo=3.0, espesor=0.2, origen=(7.0, 4.0, 15.0), material='Hormigon')