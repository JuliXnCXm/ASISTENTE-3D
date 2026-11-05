import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_terreno_plano(
    nombre="Acera",
    ancho=25.0,
    fondo=8.0,
    espesor=0.2,
    origen=(0,0,0),
    material="Asfalto"
)
A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    con_columnas=True,
    modulo_columna_x=5.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=2.2,
    ventana_alfeizar=0.5,
    ventana_separacion=2.5,
    origen=(-10, -4, 0.1),
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio",
    material_marco="Marco_Aluminio"
)