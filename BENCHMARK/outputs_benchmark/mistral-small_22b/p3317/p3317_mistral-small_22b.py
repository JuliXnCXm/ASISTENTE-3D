import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Función para crear adoquines
def create_cobblestones():
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    obj = bpy.context.object
    obj.scale = (2, 1, 1)
    for i in range(-5, 6):
        for j in range(-5, 6):
            new_obj = obj.copy()
            new_obj.location = (i * 2, j * 1, 0)
            bpy.context.collection.objects.link(new_obj)

# Función para crear bancas
def create_benches():
    for i in range(-3, 4):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 2, -6, 0))
        bench = bpy.context.object
        bench.scale = (2, 0.5, 0.5)

# Función para crear farolas
def create_lampposts():
    for i in range(-3, 4):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=5, location=(i * 2, 6, 0))
        lamppost = bpy.context.object
        lamppost.scale = (1, 1, 1)

# Función para crear árboles en alcorques cuadrados
def create_trees():
    for i in range(-2, 3):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=(i * 2, -4, 0))
        alcorque = bpy.context.object
        alcorque.scale = (1, 1, 1)
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, depth=3, location=(i * 2, -4, 2))
        tree = bpy.context.object
        tree.scale = (1, 1, 1)

# Crear geometría
create_cobblestones()
create_benches()
create_lampposts()
create_trees()

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])