import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
tamaño_mesa = 1.2
altura_mesa = 0.45
grosor_tablero = 0.05
tamaño_pata = 0.1
altura_pata = altura_mesa - grosor_tablero

# Tablero
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_pata + grosor_tablero / 2),
    scale=(tamaño_mesa, tamaño_mesa, grosor_tablero)
)

# Patas
offset = (tamaño_mesa / 2) - (tamaño_pata / 2)
posiciones_patas = [
    (offset, offset, altura_pata / 2),
    (-offset, offset, altura_pata / 2),
    (offset, -offset, altura_pata / 2),
    (-offset, -offset, altura_pata / 2)
]

for pos in posiciones_patas:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=pos,
        scale=(tamaño_pata, tamaño_pata, altura_pata)
    )