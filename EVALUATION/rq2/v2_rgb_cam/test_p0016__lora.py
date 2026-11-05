import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 1.8
profundidad = 0.3
num_estantes = 5

# Crear el cuerpo base de la estantería
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto / 2),
    scale=(ancho, profundidad, alto)
)
estanteria_base = bpy.context.active_object
estanteria_base.name = "Estanteria_Base"

# Crear los estantes
espacio_entre_estantes = alto / (num_estantes + 1)

for i in range(num_estantes):
    z_pos = (i + 1) * espacio_entre_estantes
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho, 0.01, 0.01)
    )
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1}"