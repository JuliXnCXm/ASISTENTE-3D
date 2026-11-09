import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=6, ancho=20, fondo=14, alto_piso=3, origen=(0, 0, 0))
bpy.ops.object.select_all(action='DESELECT')
ed.select_set(True)
bpy.context.view_layer.objects.active = ed
A.crear_escalera_recta(nombre='Escalera', huella=0.28, contrahuella=0.175, ancho=1.1, num_peldanos=16, grosor_peldano=0.03, con_contrahuellas=True, con_zancas=True, espesor_zanca=0.15, origen=(0, 0, 0), material='Hormigon')
A.crear_muro(nombre='Muro', largo=4.0, alto=3.0, grosor=0.2, origen=(0, 0, 0), rotacion_z=0.0, material='Muro_Generic')
A.crear_tejado_dos_aguas(nombre='Tejado', ancho=8.0, fondo=6.0, altura_cumbrera=2.5, espesor=0.15, voladizo_x=0.4, voladizo_y=0.3, origen=(0, 0, 3.0), material='Teja')
A.crear_losa_rectangular(nombre='Losa', ancho=20.0, fondo=14.0, espesor=0.3, origen=(0, 0, 0), material='Concreto_Piso')
A.crear_piso(nombre='Piso_Superior', ancho=20.0, fondo=14.0, espesor=0.3, origen=(0, 0, 6.0), material='Concreto_Piso')
A.crear_columna(nombre='Columna.001', seccion='rect', ancho=0.4, fondo=0.4, alto=6.0, origen=(-1.0, -1.0, 0.0), material='Hormigon')
A.crear_columna(nombre='Columna.002', seccion='rect', ancho=0.4, fondo=0.4, alto=6.0, origen=(1.0, -1.0, 0.0), material='Hormigon')
A.crear_columna(nombre='Columna.003', seccion='rect', ancho=0.4, fondo=0.4, alto=6.0, origen=(-1.0, 1.0, 0.0), material='Hormigon')
A.crear_columna(nombre='Columna.004', seccion='rect', ancho=0.4, fondo=0.4, alto=6.0, origen=(1.0, 1.0, 0.0), material='Hormigon')
A.crear_ventana(nombre='Ventana_Frente', ancho=19.2, alto=2.2, prof_marco=0.2, divisiones=(3, 4), origen=(0, 0, 1.4), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.crear_ventana(nombre='Ventana_Fondo', ancho=19.2, alto=2.2, prof_marco=0.2, divisiones=(3, 4), origen=(0, 14, 1.4), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.crear_ventana(nombre='Ventana_Izquierda', ancho=14.4, alto=2.2, prof_marco=0.2, divisiones=(2, 4), origen=(-10, 0, 1.4), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.crear_ventana(nombre='Ventana_Derecha', ancho=14.4, alto=2.2, prof_marco=0.2, divisiones=(2, 4), origen=(10, 0, 1.4), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.abrir_vanos_batch_rectangulares(nombre='Vanos_Ventanas', centros_world=[(-9.6, 0, 1.4), (9.6, 0, 1.4), (-10, 0, 1.4), (10, 0, 1.4)], ancho=19.2, alto=2.2)
A.asignar_material(nombre='Marco_Negro', base_color=(0.0, 0.0, 0.0, 1.0))
A.asignar_material(nombre='Vidrio', base_color=(1.0, 1.0, 1.0, 1.0))