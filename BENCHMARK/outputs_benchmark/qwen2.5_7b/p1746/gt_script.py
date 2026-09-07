import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
A.crear_terreno_plano('Base_Urbana', ancho=40, fondo=40, espesor=0.2, material='Asfalto')
A.crear_edificio_n_pisos(
    nombre='Edificio_Corporativo',
    pisos=5,
    ancho=15,
    fondo=20,
    alto_piso=3.2,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=2.5,
    ventana_alfeizar=0.4,
    ventana_separacion=2.5,
    origen=(0,0,0.1),
    material_fachada='Estuco',
    material_losa='Hormigon',
    material_vidrio='Vidrio',
    material_marco='Marco_Aluminio'
)