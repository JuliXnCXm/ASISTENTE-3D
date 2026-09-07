import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el colchón
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
colchon = bpy.context.object
colchon.name = "Colchon"

# Ajustar las dimensiones del colchón
bpy.ops.transform.resize(value=(2, 1.5, 0.3))

# Crear la estructura de madera
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -0.75, -0.6))
estructura = bpy.context.object
estructura.name = "Estructura"

# Ajustar las dimensiones de la estructura
bpy.ops.transform.resize(value=(2, 1.5, 0.3))

# Cambiar el color del colchón a blanco
colchon.active_material = bpy.data.materials.new(name="MaterialColchon")
colchon.active_material.diffuse_color = (1, 1, 1)

# Cambiar el color de la estructura a roble
estructura.active_material = bpy.data.materials.new(name="MaterialEstructura")
estructura.active_material.diffuse_color = (0.8, 0.45, 0.2)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])