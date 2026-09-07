import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el muro de ladrillo
bpy.ops.mesh.primitive_plane_add(size=20, enter_editmode=False, align='WORLD', location=(0, 0, 1.1))
wall = bpy.context.object
wall.scale = (10, 2.2, 0.2)

# Crear la puerta de madera
bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(-4.5, 0, 1))
door = bpy.context.object
door.scale = (1, 2.2, 0.1)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)