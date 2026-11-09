import blender_arch as A
import bpy
import bmesh
import math
A.limpiar_escena()
ed = A.crear_edificio_n_pisos('Edificio', pisos=5, ancho=12, fondo=14, alto_piso=3, origen=(0, 0, 0))
bpy.ops.object.select_all(action='DESELECT')
ed.select_set(True)
bpy.context.view_layer.objects.active = ed
A.crear_escalera_recta(nombre='Escalera', huella=0.28, contrahuella=0.175, ancho=1.1, num_peldanos=16, grosor_peldano=0.03, con_contrahuellas=True, con_zancas=True, espesor_zanca=0.15, origen=(0, 0, 0), material='Hormigon')
A.crear_muro(nombre='Muro', largo=4.0, alto=3.0, grosor=0.2, origen=(0, 0, 0), rotacion_z=0.0, material='Muro_Generic')
A.crear_tejado_dos_aguas(nombre='Tejado', ancho=8.0, fondo=6.0, altura_cumbrera=2.5, espesor=0.15, voladizo_x=0.4, voladizo_y=0.3, origen=(0, 0, 3.0), material='Teja')
A.crear_losa_rectangular(nombre='Losa', ancho=12.0, fondo=14.0, espesor=0.3, origen=(0, 0, 0), material='Concreto_Piso')
A.crear_piso(nombre='Piso_Superior', ancho=12.0, fondo=14.0, espesor=0.3, origen=(0, 0, 3.0), material='Parquet')
A.crear_columna(nombre='Columna.001', seccion='rect', ancho=0.4, fondo=0.4, alto=3.0, origen=(-3, -3, 0), material='Hormigon')
A.crear_columna(nombre='Columna.002', seccion='rect', ancho=0.4, fondo=0.4, alto=3.0, origen=(3, -3, 0), material='Hormigon')
A.crear_columna(nombre='Columna.003', seccion='rect', ancho=0.4, fondo=0.4, alto=3.0, origen=(-3, 3, 0), material='Hormigon')
A.crear_columna(nombre='Columna.004', seccion='rect', ancho=0.4, fondo=0.4, alto=3.0, origen=(3, 3, 0), material='Hormigon')
A.crear_ventana(nombre='Ventana_Frente', ancho=5.0, alto=1.5, prof_marco=0.2, origen=(0, 0, 1.5), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.crear_ventana(nombre='Ventana_Fondo', ancho=5.0, alto=1.5, prof_marco=0.2, origen=(0, 14, 1.5), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.crear_ventana(nombre='Ventana_Izquierda', ancho=14.0, alto=1.5, prof_marco=0.2, origen=(0, 0, 1.5), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.crear_ventana(nombre='Ventana_Derecha', ancho=14.0, alto=1.5, prof_marco=0.2, origen=(12, 0, 1.5), material_marco='Marco_Negro', material_vidrio='Vidrio')
A.crear_puerta(nombre='Puerta_Acceso', ancho=1.0, alto=2.1, prof_marco=0.2, origen=(0, 0, 0.9), material_marco='Marco_Negro', material_panel='Madera_Roble')
A.crear_sofa(nombre='Sofa', ancho=2.0, fondo=0.9, origen=(5, 6, 0), material='Tela_Gris')
A.crear_silla(nombre='Silla.001', origen=(0, 0, 0), material='Cuero')
A.crear_silla(nombre='Silla.002', origen=(12, 0, 0), material='Cuero')
A.crear_luz(nombre='Luz_Principal', tipo='AREA', ubicacion=(6, 7, 7), energia=200, color=(1.0, 0.9, 0.8))
A.crear_camara(nombre='Camara', ubicacion=(6, -10, 5), rotacion=(75, 0, 0))