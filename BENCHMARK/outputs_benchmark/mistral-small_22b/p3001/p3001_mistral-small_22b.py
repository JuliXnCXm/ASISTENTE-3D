import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Función para crear una pared
def create_wall(location, size):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.object
    obj.scale.x = size[0] / 2
    obj.scale.y = size[1] / 2
    obj.scale.z = size[2] / 2
    return obj

# Crear paredes exteriores
create_wall(location=(0, 0, 0), size=(5, 3, 3))  # Pared frontal
create_wall(location=(10, 0, 0), size=(5, 3, 3))  # Pared trasera
create_wall(location=(0, 0, 3), size=(15, 3, 3))  # Pared izquierda
create_wall(location=(0, 0, -3), size=(15, 3, 3))  # Pared derecha

# Crear paredes interiores
create_wall(location=(7.5, 0, 0), size=(2.5, 3, 3))  # Pared interior frontal
create_wall(location=(7.5, 0, -6), size=(2.5, 3, 3))  # Pared interior trasera
create_wall(location=(0, 0, -3), size=(15, 3, 3))  # Pared izquierda interior
create_wall(location=(15, 0, -3), size=(15, 3, 3))  # Pared derecha interior

# Crear techo
bpy.ops.mesh.primitive_cube_add(size=(15, 6, 3), location=(7.5, 3, -3))
obj = bpy.context.object
obj.scale.x = 15 / 2
obj.scale.y = 6 / 2
obj.scale.z = 3 / 2

# Crear suelo
bpy.ops.mesh.primitive_cube_add(size=(15, 0.3, 6), location=(7.5, -1.5, -3))
obj = bpy.context.object
obj.scale.x = 15 / 2
obj.scale.y = 0.3 / 2
obj.scale.z = 6 / 2

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])