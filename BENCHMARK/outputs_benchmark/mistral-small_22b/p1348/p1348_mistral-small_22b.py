import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el terreno plano
bpy.ops.mesh.primitive_plane_add(size=15, location=(0, 0, 0))
terreno = bpy.context.object

# Añade un material de césped al terreno
material = bpy.data.materials.new(name="Césped")
material.diffuse_color = (0, 1, 0, 1)  # Color verde
terreno.data.materials.append(material)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as(filepath=os.environ['BLEND_OUT'])