import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 1.75, 0))
bpy.context.object.name = "Suelo"
bpy.context.object.data.materials.append(bpy.data.materials.new(name="Parquet"))
bpy.context.object.data.materials[0].diffuse_color = (0.8, 0.4, 0.2)

# Crea las paredes
for x in [-2, 2]:
    for z in [-1.75, 1.75]:
        bpy.ops.mesh.primitive_cube_add(size=3.5, location=(x, 0, z))
        bpy.context.object.name = "Pared"
        bpy.context.object.data.materials.append(bpy.data.materials.new(name="Gris"))
        bpy.context.object.data.materials[0].diffuse_color = (0.5, 0.5, 0.5)

# Crea la cama doble
bpy.ops.mesh.primitive_cube_add(size=2, location=(1, 0.75, -0.8))
bpy.context.object.name = "Cama"
bpy.context.object.data.materials.append(bpy.data.materials.new(name="Madera"))
bpy.context.object.data.materials[0].diffuse_color = (0.6, 0.35, 0.2)

# Crea el armario de dos puertas
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0.75, -2))
bpy.context.object.name = "Armario"
bpy.context.object.data.materials.append(bpy.data.materials.new(name="Madera"))
bpy.context.object.data.materials[0].diffuse_color = (0.6, 0.35, 0.2)

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])