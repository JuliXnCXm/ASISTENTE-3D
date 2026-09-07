import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear un bolardo cilíndrico
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.9, location=(0, 0, 0))

# Renombrar el objeto al bolardo
bpy.context.object.name = "Bolardo"

# Guardar la escena si se proporciona BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene['BLEND_OUT'])