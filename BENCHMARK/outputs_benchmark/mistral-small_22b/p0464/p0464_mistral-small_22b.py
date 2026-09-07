import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo de concreto
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 2, 0))
concrete = bpy.context.object
concrete.name = "Concrete Floor"

# Crear el muro de ladrillo
bpy.ops.mesh.primitive_cube_add(size=4, location=(0, -2, 4))
wall = bpy.context.object
wall.name = "Brick Wall"

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])