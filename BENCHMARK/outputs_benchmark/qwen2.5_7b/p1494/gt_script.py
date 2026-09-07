import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

muro_frontal = A.crear_muro(
    nombre="Muro.Cerramiento",
    largo=10.0,
    alto=2.2,
    grosor=0.2,
    material="Ladrillo_Rojo"
)

A.crear_puerta(
    nombre="Puerta.Entrada",
    ancho=1.0,
    alto=2.0,
    prof_marco=0.2,
    origen=(4.5, 0, 0),
    material_panel="Madera_Roble",
    material_marco="Acero_Inox"
)

A.abrir_vanos_batch_rectangulares(
    muro=muro_frontal,
    centros_world=[(5.0, 0, 1.0)],
    ancho=1.0,
    alto=2.0
)