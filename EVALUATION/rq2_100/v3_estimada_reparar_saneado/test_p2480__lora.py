import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 1.8
profundidad = 0.3
num_estantes = 5

# Crear marco exterior
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto / 2))
marco = bpy.context.active_object
marco.name = 'Estanteria_Marco'
marco.dimensions = (ancho, profundidad, alto)

# Crear estantes interiores
espacio_entre_estantes = alto / (num_estantes + 1)
for i in range(num_estantes):
    z_pos = i * espacio_entre_estantes + (alto / (num_estantes + 1)) / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos)
    )
    estante = bpy.context.active_object
    estante.name = f'Estanteria_Estante_{i+1}'
    estante.dimensions = (ancho - 0.05, profundidad - 0.05, 0.05) # Un poco menos profundo para que queden bien ajustados