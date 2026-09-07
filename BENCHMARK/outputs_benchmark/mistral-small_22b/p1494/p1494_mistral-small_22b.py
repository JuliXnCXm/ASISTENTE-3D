import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el muro de ladrillo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
muro = bpy.context.object
muro.scale = (2.2, 10, 0.3)  # Altura: 2.2 m, Largo: 10 m, Grosor: 0.3 m

# Crear la puerta de madera
bpy.ops.mesh.primitive_cube_add(size=1, location=(5, 0, -0.1))  # Centrada en el muro
puerta = bpy.context.object
puerta.scale = (1, 2.2, 0.3)  # Ancho: 1 m, Altura: 2.2 m, Grosor: 0.3 m

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])