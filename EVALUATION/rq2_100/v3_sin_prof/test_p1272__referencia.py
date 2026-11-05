import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_terreno_plano(
    nombre="Plaza_Edificio",
    ancho=40.0,
    fondo=30.0,
    espesor=0.2,
    origen=(-20, -15, -0.2),
    material="Concreto_Piso"
)

A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    con_columnas=True,
    dim_columna=0.5,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(-10, -7.5, 0),
    material_fachada="Estuco",
    material_losa="Hormigon",
    material_vidrio="Vidrio",
    material_marco="Marco_Aluminio"
)