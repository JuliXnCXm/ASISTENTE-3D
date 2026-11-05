import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 1.8
profundidad = 0.3
num_estantes = 5

# Crear el cuerpo principal de la estantería
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto / 2),
    scale=(ancho, profundidad, alto)
)
estanteria = bpy.context.active_object
estanteria.name = "Estanteria"

# Crear los estantes interiores
espacio_entre_estantes = alto / (num_estantes + 1)
for i in range(num_estantes):
    z_pos = i * espacio_entre_estantes + (alto / (num_estantes + 1)) / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho - 0.02, profundidad - 0.02, 0.02)
    )
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1}"