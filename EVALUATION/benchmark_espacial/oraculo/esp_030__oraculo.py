import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=4, ancho=18, fondo=12, alto_piso=3, origen=(0, 0, 0))
anexo = A.crear_edificio_n_pisos('Anexo', pisos=1, ancho=4, fondo=5, alto_piso=3, origen=(18, 3.5, 0))
