import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el tramo de acera
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
acera = bpy.context.active_object
acera.scale = (2, 10, 0.1)  # Ancho de 2 metros y largo de 10 metros

# Crea la calzada de asfalto
bpy.ops.mesh.primitive_cube_add(size=1, location=(3, 0, 0))
calzada = bpy.context.active_object
calzada.scale = (2, 10, 0.1)  # Ancho de 2 metros y largo de 10 metros

# Crea la baranda metálica
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=10, location=(1, 0, 0))
baranda = bpy.context.active_object
baranda.scale = (2, 1, 1)  # Ajusta la escala para que cubra toda la acera

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])