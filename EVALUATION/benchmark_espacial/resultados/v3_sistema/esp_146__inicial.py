import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=16, fondo=10, alto_piso=3, origen=(0, 0, 0))
ancho_fachada = ed.dimensions[0]
fondo_fachada = ed.dimensions[2]
alto_piso = ed.pisos[2].dimensions[2]
origen_piso_3 = (0, -fondo_fachada / 2, alto_piso * 3)
A.crear_losa_rectangular('Balcon_Voladizo', ancho=3.0, fondo=1.5, espesor=0.2, origen=origen_piso_3, material='Hormigon')
A.crear_baranda_lineal('Baranda_Sur', largo=3.0, origen=(0, -fondo_fachada / 2 + 1.5 / 2, alto_piso * 3), material='Acero_Inox')