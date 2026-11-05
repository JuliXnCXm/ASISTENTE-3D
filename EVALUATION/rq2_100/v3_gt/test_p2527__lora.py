import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 2.0
profundidad = 0.3
num_baldas = 5

# Crear el cuerpo principal
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto / 2),
    scale=(ancho, profundidad, alto)
)
cuerpo = bpy.context.active_object
cuerpo.name = "Estanteria_Cuerpo"

# Crear las baldas
espacio_entre_baldas = alto / (num_baldas + 1)

for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + (espacio_entre_baldas / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho, profundidad * 0.9, profundidad * 0.05)
    )
    balda = bpy.context.active_object
    balda.name = f"Balda_{i+1}"