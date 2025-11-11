import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
tamaño_mesa = 0.8
altura_mesa = 0.45
espesor_tablero = 0.05
lado_pata = 0.07
altura_pata = altura_mesa - espesor_tablero

# Crear tablero
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, altura_mesa - espesor_tablero / 2))
tablero = bpy.context.active_object
tablero.name = 'TableroMesa'
tablero.dimensions = (tamaño_mesa, tamaño_mesa, espesor_tablero)

# Crear patas
distancia_pata = (tamaño_mesa / 2) - (lado_pata / 2) - 0.02 # Un pequeño margen
posiciones_patas = [
    (distancia_pata, distancia_pata, altura_pata / 2),
    (-distancia_pata, distancia_pata, altura_pata / 2),
    (distancia_pata, -distancia_pata, altura_pata / 2),
    (-distancia_pata, -distancia_pata, altura_pata / 2)
]

for i, pos in enumerate(posiciones_patas):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    pata = bpy.context.active_object
    pata.name = f'PataMesa_{i+1}'
    pata.dimensions = (lado_pata, lado_pata, altura_pata)