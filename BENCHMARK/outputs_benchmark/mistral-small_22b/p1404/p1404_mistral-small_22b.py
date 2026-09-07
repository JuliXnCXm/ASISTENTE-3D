import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el muro de contención
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
wall = bpy.context.object
wall.scale = (10, 1.2, 0.3)  # Longitud: 10m, Altura: 1.2m, Grosor: 0.3m

# Crear la baranda metálica
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=10, location=(0, 1.2, 0))
railing = bpy.context.object
railing.rotation_euler = (1.5708, 0, 0)  # Rotar 90 grados para que quede horizontal

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])