import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el terreno
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
terrain = bpy.context.object
terrain.scale = (15, 15, 1)

# Añadir material de césped
material = bpy.data.materials.new(name="GrassMaterial")
material.diffuse_color = (0, 1, 0, 1)
terrain.data.materials.append(material)

# Si existe la variable de entorno BLEND_OUT, guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])