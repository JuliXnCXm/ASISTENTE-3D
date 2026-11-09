import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=5, ancho=20, fondo=12, alto_piso=3, origen=(0, 0, 0))
A.crear_escalera_recta('EscaleraExterior', huella=0.28, contrahuella=0.1765, ancho=1.1, num_peldanos=17, origen=(7.62, 12.1, 0))
