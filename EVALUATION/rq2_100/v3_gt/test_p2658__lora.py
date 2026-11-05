import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho_total = 1.2
alto_total = 2.0
profundidad_total = 0.3
num_estantes = 5

ancho_estante = ancho_total / num_estantes
alto_estante = alto_total / num_estantes

for i in range(num_estantes):
    pos_z = i * alto_estante + alto_estante / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, pos_z),
        scale=(ancho_estante, profundidad_total, alto_estante)
    )
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1}"