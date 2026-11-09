import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=10, fondo=10, alto_piso=3, origen=(0, 0, 0))
atico = A.crear_edificio_n_pisos('Atico', pisos=1, ancho=5, fondo=3, alto_piso=3, origen=(2.5, 3.5, 0))
atico.location.z = 18.2
