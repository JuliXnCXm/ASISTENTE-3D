import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

muro_jardin = A.crear_muro(
    nombre="Muro_Perimetral",
    largo=8.0,
    alto=2.2,
    grosor=0.15,
    material="Ladrillo_Rojo"
)

origen_puerta = (3.5, 0, 0)
A.crear_puerta(
    nombre="Puerta_Jardin",
    ancho=1.0,
    alto=2.0,
    prof_marco=0.15,
    origen=origen_puerta,
    material_panel="Madera_Roble",
    material_marco="Marco_Negro"
)

centro_vano_world = (4.0, 0, 1.0)
A.abrir_vanos_batch_rectangulares(
    muro=muro_jardin,
    centros_world=[centro_vano_world],
    ancho=1.0,
    alto=2.0
)