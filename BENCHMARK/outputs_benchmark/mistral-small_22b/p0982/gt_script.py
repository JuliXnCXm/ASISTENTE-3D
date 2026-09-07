import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_sofa(
    nombre="SofaPrincipal",
    ancho=2.4,
    fondo=0.9,
    alto_asiento=0.42,
    origen=(0, 0, 0),
    material="Cuero"
)

A.crear_mesa(
    nombre="MesaCentro",
    ancho=1.2,
    fondo=0.6,
    alto=0.45,
    origen=(0, -1.2, 0),
    material_tablero="Madera_Nogal"
)