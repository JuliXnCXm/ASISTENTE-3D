import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el primer muro (4m de largo, 2.5m de alto)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
muro1 = bpy.context.object
muro1.scale.x = 4
muro1.scale.y = 2.5

# Crea el segundo muro (3m de largo, 2.5m de alto)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 3, 0))
muro2 = bpy.context.object
muro2.scale.y = 2.5
muro2.scale.z = 3

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])