import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el muro perimetral
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 4, 0))
muro = bpy.context.object
muro.scale = (8, 2.2, 0.3)  # Longitud: 8m, Altura: 2.2m, Grosor: 0.3m

# Crear la puerta de madera
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 4, -0.15))
puerta = bpy.context.object
puerta.scale = (1, 2.2, 0.3)  # Ancho: 1m, Altura: 2.2m, Grosor: 0.3m

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])