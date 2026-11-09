import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=10, fondo=8, alto_piso=3, origen=(0, 0, 0))
anexo = A.crear_edificio_n_pisos('Anexo', pisos=1, ancho=5, fondo=4, alto_piso=3, origen=(2.5, -4, 0))
