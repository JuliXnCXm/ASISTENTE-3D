import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=3, ancho=10, fondo=12, alto_piso=3, origen=(0, 0, 0))
ed.rotation_euler.z = math.radians(-25)
