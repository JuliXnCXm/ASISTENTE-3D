import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

ancho = 4.0
fondo = 3.0
alto = 2.5

A.crear_columna(nombre='Columna_NE', seccion='rect', ancho=0.2, fondo=0.2, alto=alto, origen=(ancho/2, fondo/2, 0), material='Madera_Roble')
A.crear_columna(nombre='Columna_NO', seccion='rect', ancho=0.2, fondo=0.2, alto=alto, origen=(-ancho/2, fondo/2, 0), material='Madera_Roble')
A.crear_columna(nombre='Columna_SE', seccion='rect', ancho=0.2, fondo=0.2, alto=alto, origen=(ancho/2, -fondo/2, 0), material='Madera_Roble')
A.crear_columna(nombre='Columna_SO', seccion='rect', ancho=0.2, fondo=0.2, alto=alto, origen=(-ancho/2, -fondo/2, 0), material='Madera_Roble')

A.crear_techo_plano(nombre='Cubierta_Pergola', ancho=ancho, fondo=fondo, espesor=0.15, origen=(0, 0, alto), material='Madera_Roble')