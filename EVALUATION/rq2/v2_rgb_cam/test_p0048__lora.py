import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_techo_plano(
    nombre="TechoReticular",
    ancho=6.0,
    fondo=4.0,
    espesor=0.05,
    material="Marco_Negro"
)

A.agregar_luz(
    nombre="Luz_Techo_1",
    tipo="POINT",
    ubicacion=(-2.5, 2.0, 2.8),
    energia=150
)
A.agregar_luz(
    nombre="Luz_Techo_2",
    tipo="POINT",
    ubicacion=(2.5, 2.0, 2.8),
    energia=150
)
A.agregar_luz(
    nombre="Luz_Techo_3",
    tipo="POINT",
    ubicacion=(-2.5, -2.0, 2.8),
    energia=150
)
A.agregar_luz(
    nombre="Luz_Techo_4",
    tipo="POINT",
    ubicacion=(2.5, -2.0, 2.8),
    energia=150
)