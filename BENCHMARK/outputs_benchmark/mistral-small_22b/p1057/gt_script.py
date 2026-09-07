import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_escalera_recta(
    nombre="Escalera_Principal", 
    ancho=1.0, 
    num_peldanos=16, 
    con_contrahuellas=True, 
    material="Hormigon"
)