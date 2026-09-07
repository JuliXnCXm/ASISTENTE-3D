import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_edificio_n_pisos(
    nombre="Edificio_Residencial",
    pisos=4,
    ancho=15.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.2,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=5.0,
    modulo_columna_y=6.0,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.2,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    material_fachada="Ladrillo",
    material_losa="Hormigon",
    material_vidrio="Vidrio",
    material_marco="Marco_Blanco"
)