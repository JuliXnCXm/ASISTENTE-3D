import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=3, ancho=12, fondo=10, alto_piso=3, origen=(0, 0, 0))
anexo = A.crear_edificio_n_pisos('Anexo', pisos=1, ancho=3, fondo=4, alto_piso=3, origen=(-3, 3, 0))
