import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_terreno_plano(
    nombre="Parcela_Tierra",
    ancho=5.0,
    fondo=5.0,
    espesor=0.2,
    material="Terreno"
)

A.crear_arbol_simple(
    nombre="Arbol_Central",
    radio_copa=2.0,
    altura_copa=3.5,
    altura_tronco=2.0,
    origen=(0, 0, 0.1)
)