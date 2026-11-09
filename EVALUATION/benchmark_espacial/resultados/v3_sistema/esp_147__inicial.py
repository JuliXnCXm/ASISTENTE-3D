import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=5, ancho=10, fondo=14, alto_piso=3, origen=(0, 0, 0))
bpy.ops.object.select_all(action='DESELECT')
ed.select_set(True)
bpy.context.view_layer.objects.active = ed
A.rotar_objeto(ed, -30, 'Z')