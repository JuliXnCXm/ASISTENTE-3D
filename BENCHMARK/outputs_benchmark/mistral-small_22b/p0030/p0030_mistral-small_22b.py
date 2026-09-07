import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el muro interior
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.7 / 2))
wall = bpy.context.object

# Escala el cubo para ajustar las dimensiones del muro
wall.scale = (5, 0.15, 2.7)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])