import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear un bolardo cilíndrico
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.9, location=(0, 0, 0))

# Renombrar el objeto al bolardo
bpy.context.object.name = "Bolardo"

# Guardar la escena si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)