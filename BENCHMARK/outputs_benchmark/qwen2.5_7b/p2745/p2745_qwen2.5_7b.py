import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear un bolardo cilíndrico
radius = 0.15  # Radio (mitad del diámetro)
height = 0.9   # Altura

# Crear el objeto cilíndro
bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=(0, 0, 0))

# Renombrar el objeto al bolardo
cylinder_obj = bpy.context.object
cylinder_obj.name = "Bolardo"

# Guardar la escena si se proporciona BLEND_OUT
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)