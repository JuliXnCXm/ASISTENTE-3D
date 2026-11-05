import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 2.0
fondo = 0.3
num_baldas = 5

# Dimensiones de cada balda
grosor_balda = 0.02
ancho_balda = ancho - grosor_balda * 2
alto_balda = alto / num_baldas

# Crear el cuerpo base
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_balda / 2),
    scale=(ancho, fondo, alto_balda)
)
base = bpy.context.active_object
base.name = "BaseEstanteria"

# Crear las baldas
espacio_entre_baldas = alto_balda * (num_baldas - 1)

for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + alto_balda / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_balda, fondo, grosor_balda)
    )
    balda = bpy.context.active_object
    balda.name = f"Balda_{i+1}"