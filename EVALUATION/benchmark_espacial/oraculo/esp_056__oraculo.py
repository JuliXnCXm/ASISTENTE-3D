import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=3, ancho=16, fondo=14, alto_piso=3, origen=(0, 0, 0))
atico = A.crear_edificio_n_pisos('Atico', pisos=1, ancho=5, fondo=3, alto_piso=3, origen=(5.5, 5.5, 0))
atico.location.z = 9.2
