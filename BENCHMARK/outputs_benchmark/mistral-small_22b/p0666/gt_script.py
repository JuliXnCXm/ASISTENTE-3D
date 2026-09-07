import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Crear sofá de 3 plazas
A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.2,
    fondo=0.9,
    origen=(0, 0, 0),
    material="Tela_Gris"
)

# Crear mesa de centro frente al sofá
A.crear_mesa(
    nombre="Mesa_Centro",
    ancho=1.2,
    fondo=0.6,
    alto=0.45,
    origen=(0, 1.5, 0),
    material_tablero="Madera_Nogal"
)