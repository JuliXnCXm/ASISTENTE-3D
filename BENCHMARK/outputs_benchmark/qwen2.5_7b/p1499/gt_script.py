import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Terreno
A.crear_terreno_plano(
    nombre="Zona_Verde",
    ancho=15.0,
    fondo=10.0,
    material="Cesped"
)

# Árbol
A.crear_arbol_simple(
    nombre="Arbol_Parque",
    origen=(-4, -2, 0)
)

# Banco (usando una mesa estrecha)
A.crear_mesa(
    nombre="Banco_Parque",
    ancho=1.8,
    fondo=0.5,
    alto=0.45,
    origen=(2, 1, 0),
    material_tablero="Madera_Roble"
)