import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
tamaño_mesa = 1.2
altura_total = 0.45
grosor_tablero = 0.05
altura_patas = altura_total - grosor_tablero
tamaño_pata = 0.10
offset_patas = tamaño_mesa / 2 - tamaño_pata / 2

# Crear tablero
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_patas + grosor_tablero / 2),
    scale=(tamaño_mesa, tamaño_mesa, grosor_tablero)
)
bpy.context.object.name = "TableroMesa"

# Crear patas
posiciones_patas = [
    (offset_patas, offset_patas, altura_patas / 2),
    (-offset_patas, offset_patas, altura_patas / 2),
    (offset_patas, -offset_patas, altura_patas / 2),
    (-offset_patas, -offset_patas, altura_patas / 2)
]

for i, pos in enumerate(posiciones_patas):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=pos,
        scale=(tamaño_pata, tamaño_pata, altura_patas)
    )
    bpy.context.object.name = f"PataMesa_{i+1}"