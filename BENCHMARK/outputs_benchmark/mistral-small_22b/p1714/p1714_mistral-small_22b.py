import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el muro de ladrillo rojo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
muro = bpy.context.object
muro.scale = (10, 2.5, 0.3)  # Longitud: 10 m, Altura: 2.5 m, Grosor: 0.3 m
muro.name = "Muro"

# Crea la puerta de madera
bpy.ops.mesh.primitive_cube_add(size=1, location=(4.75, 0, -1.2))  # Centrada en el muro
puerta = bpy.context.object
puerta.scale = (1.5, 2.5, 0.3)  # Ancho: 1.5 m, Altura: 2.5 m, Grosor: 0.3 m
puerta.name = "Puerta"

# Cambia el color del muro a rojo
muro_material = bpy.data.materials.new(name="MuroMaterial")
muro_material.diffuse_color = (1, 0, 0)  # Rojo
muro.data.materials.append(muro_material)

# Cambia el color de la puerta a marrón
puerta_material = bpy.data.materials.new(name="PuertaMaterial")
puerta_material.diffuse_color = (0.8, 0.4, 0.2)  # Marrón
puerta.data.materials.append(puerta_material)

# Guarda el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])