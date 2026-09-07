import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_cama(
    nombre="CamaDoble",
    ancho=1.6,
    largo=2.0,
    alto_cabecero=1.0,
    origen=(0, 0, 0),
    material_colchon="Textil_Blanco",
    material_base="Madera_Roble"
)