import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=4, ancho=16, fondo=8, alto_piso=3, origen=(0, 0, 0))
bpy.ops.object.select_all(action='DESELECT')
ed.select_set(True)
bpy.context.view_layer.objects.active = ed
A.crear_escalera_recta(nombre='Escalera', huella=0.28, contrahuella=0.175, ancho=1.1, num_peldanos=16, grosor_peldano=0.03, con_contrahuellas=True, con_zancas=True, espesor_zanca=0.15, origen=(0, 0, 0), material='Hormigon')
A.crear_muro(nombre='Muro', largo=4.0, alto=3.0, grosor=0.2, origen=(0, 0, 0), rotacion_z=0.0, material='Muro_Generic')
A.crear_tejado_dos_aguas(nombre='Tejado', ancho=8.0, fondo=6.0, altura_cumbrera=2.5, espesor=0.15, voladizo_x=0.4, voladizo_y=0.3, origen=(0, 0, 3.0), material='Teja')
A.crear_losa_rectangular(nombre='Losa_Piso', ancho=16.0, fondo=8.0, espesor=0.3, origen=(0, 0, 0), material='Concreto_Piso')
A.crear_piso(nombre='Piso_Superior', ancho=16.0, fondo=8.0, espesor=0.3, origen=(0, 0, 3.0), material='Parquet')