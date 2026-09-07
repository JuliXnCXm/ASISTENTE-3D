import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
bpy.context.object.scale = (4, 3, 0.1)

# Crear las columnas
column_locations = [
    (-2, -1.5),
    (2, -1.5),
    (-2, 1.5),
    (2, 1.5)
]

for loc in column_locations:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=2.5, location=loc)

# Crear el techo
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 2.5))
bpy.context.object.scale = (4, 3, 1)

# Guardar el archivo si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])