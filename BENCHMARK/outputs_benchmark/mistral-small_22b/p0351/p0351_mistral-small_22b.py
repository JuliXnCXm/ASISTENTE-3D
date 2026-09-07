import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el marco de la cama
def create_frame():
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    frame = bpy.context.object
    frame.name = "Frame"

    # Crear los postes
    for i in range(4):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2, location=(i * 2 - 2, 0, 0))
        post = bpy.context.object
        post.name = f"Post_{i}"
        frame.objects.link(post)

    # Crear las tablas
    for i in range(2):
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, i * 2 - 2, 1))
        table = bpy.context.object
        table.name = f"Table_{i}"
        frame.objects.link(table)

create_frame()

# Crear el colchón
def create_mattress():
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    mattress = bpy.context.object
    mattress.name = "Mattress"
    mattress.data.materials.append(bpy.data.materials.new(name="WhiteMaterial"))
    mattress.data.materials[0].diffuse_color = (1, 1, 1)

create_mattress()

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as(filepath=os.environ['BLEND_OUT'])