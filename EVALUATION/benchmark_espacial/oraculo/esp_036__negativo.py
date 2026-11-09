import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=10, fondo=10, alto_piso=3, origen=(0, 0, 0))
A.crear_escalera_recta('EscaleraExterior', huella=0.28, contrahuella=0.1765, ancho=1.1, num_peldanos=17, origen=(2.62, 10.1, 0))
