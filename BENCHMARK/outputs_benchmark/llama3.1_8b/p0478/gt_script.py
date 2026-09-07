import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
A.crear_edificio_n_pisos(
    'Edificio_Oficinas',
    pisos=5,
    ancho=20.0,
    fondo=15.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    ventanas_fachada=True,
    ventana_ancho=2.0,
    ventana_alto=2.0,
    ventana_alfeizar=0.6,
    ventana_separacion=2.8,
    material_fachada='Muro_Pintura_Gris',
    material_losa='Hormigon',
    material_vidrio='Vidrio',
    material_marco='Marco_Aluminio'
)