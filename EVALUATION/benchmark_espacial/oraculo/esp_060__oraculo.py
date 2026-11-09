import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=5, ancho=18, fondo=12, alto_piso=3, origen=(0, 0, 0))
atico = A.crear_edificio_n_pisos('Atico', pisos=1, ancho=5, fondo=4, alto_piso=3, origen=(6.5, 4, 0))
atico.location.z = 15.2
