import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
sofa = bpy.context.object
sofa.scale = (2, 1, 1)

# Crear la alfombra
bpy.ops.mesh.primitive_plane_add(size=3, location=(0, 0, -0.5))
carpet = bpy.context.object
carpet.scale = (2, 1, 1)

# Crear el mueble de TV
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, -1.5, -1))
tv_stand = bpy.context.object
tv_stand.scale = (2, 0.5, 1)

# Crear el panel de listones de madera vertical
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, -3, -2))
panel = bpy.context.object
panel.scale = (1, 0.5, 1)

# Guardar el archivo si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])