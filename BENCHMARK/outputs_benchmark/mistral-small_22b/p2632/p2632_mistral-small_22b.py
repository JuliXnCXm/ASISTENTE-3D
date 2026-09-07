import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea la columna interior
bpy.ops.mesh.primitive_cube_add(size=0.4, location=(0, 0, 1.4))
column = bpy.context.object

# Ajusta la altura de la columna
column.scale.z = 7

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])