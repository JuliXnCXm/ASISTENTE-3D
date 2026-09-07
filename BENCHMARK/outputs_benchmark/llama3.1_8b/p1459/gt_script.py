import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)

A.crear_edificio_n_pisos(
    nombre="EdificioCorporativo", 
    pisos=4, 
    ancho=20.0, 
    fondo=15.0, 
    alto_piso=3.2, 
    grosor_muro=0.3, 
    con_techo_plano=True, 
    con_columnas=True, 
    dim_columna=0.4, 
    modulo_columna_x=5.0, 
    modulo_columna_y=5.0, 
    ventanas_fachada=True, 
    ventana_ancho=1.8, 
    ventana_alto=1.5, 
    ventana_alfeizar=1.0, 
    ventana_separacion=3.0, 
    material_fachada="Hormigon", 
    material_losa="Concreto_Piso", 
    material_vidrio="Vidrio_Templado", 
    material_marco="Marco_Aluminio"
)