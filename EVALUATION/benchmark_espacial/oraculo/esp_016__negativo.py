import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=5, ancho=20, fondo=8, alto_piso=3, origen=(0, 0, 0))
_e = A.crear_escalera_recta('EscaleraExterior', huella=0.28, contrahuella=0.1765, ancho=1.1, num_peldanos=17, origen=(-0.1, 1.62, 0))
_e.rotation_euler.z = math.pi / 2
