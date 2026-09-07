import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)

A.crear_tejado_dos_aguas(
    nombre="Tejado_Caseta", 
    ancho=4.0, 
    fondo=3.0, 
    altura_cumbrera=1.2, 
    espesor=0.15, 
    voladizo_x=0.3, 
    voladizo_y=0.3, 
    origen=(0,0,0), 
    material="Teja"
)