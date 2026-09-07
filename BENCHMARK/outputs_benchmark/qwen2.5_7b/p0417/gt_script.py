import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_sofa(
    nombre="SofaPrincipal", 
    ancho=2.4, 
    fondo=0.95, 
    alto_asiento=0.45, 
    origen=(0, 0, 0), 
    material="Tela_Gris"
)
A.crear_mesa(
    nombre="MesaCentro", 
    ancho=1.2, 
    fondo=0.6, 
    alto=0.4, 
    origen=(0, 1.8, 0), 
    material_tablero="Madera"
)