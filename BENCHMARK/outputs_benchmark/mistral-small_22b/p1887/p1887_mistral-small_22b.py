import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Función para crear el escritorio en forma de L
def create_desk():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    desk = bpy.context.object
    desk.scale = (2, 0.5, 0.7)
    bpy.ops.transform.rotate(value=-1.5708, orient_axis='X')

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -2, 0))
    desk_leg = bpy.context.object
    desk_leg.scale = (0.7, 0.7, 0.5)

    # Unir los objetos en uno solo
    bpy.ops.object.select_all(action='DESELECT')
    desk.select_set(True)
    desk_leg.select_set(True)
    bpy.context.view_layer.objects.active = desk
    bpy.ops.object.join()

# Función para crear la silla de oficina
def create_chair():
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=(2, 0, 0))
    chair = bpy.context.object
    chair.scale = (0.7, 0.7, 0.7)

# Función para crear la estantería de pared con modificadores
def create_shelf():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(3, 0, 2))
    shelf = bpy.context.object
    shelf.scale = (0.5, 1, 0.1)

    # Añadir modificador de array
    bpy.ops.object.modifier_add(type='ARRAY')
    array_mod = shelf.modifiers['Array']
    array_mod.count = 5
    array_mod.relative_offset_displace[0] = 1

# Crear los objetos
create_desk()
create_chair()
create_shelf()

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])