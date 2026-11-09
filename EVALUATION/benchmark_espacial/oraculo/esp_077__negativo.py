import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=3, ancho=14, fondo=12, alto_piso=3, origen=(0, 0, 0))
