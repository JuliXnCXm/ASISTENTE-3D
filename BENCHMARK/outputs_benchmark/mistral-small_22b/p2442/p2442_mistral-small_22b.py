import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el primer muro (4m de largo sobre el eje X)
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0, 1.25))
wall1 = bpy.context.object
wall1.scale.x = 4

# Crea el segundo muro (3m de largo sobre el eje Y)
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 1.5, 1.25))
wall2 = bpy.context.object
wall2.scale.y = 3

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])