import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
width = 4.0
length = 3.0
height = 2.5

# Crear postes cuadrados de 15x15 cm
post_size = 0.15

# Posiciones de los postes
post_positions = [
    (-width / 2 + post_size / 2, -length / 2 + post_size / 2, height / 2),
    (width / 2 - post_size / 2, -length / 2 + post_size / 2, height / 2),
    (-width / 2 + post_size / 2, length / 2 - post_size / 2, height / 2),
    (width / 2 - post_size / 2, length / 2 - post_size / 2, height / 2)
]

# Crear los postes
for pos in post_positions:
    bpy.ops.mesh.primitive_cube_add(size=post_size, location=pos)

# Crear la estructura de la pérgola
bpy.ops.mesh.primitive_cube_add(size=width, location=(-width / 2, -length / 2, height))
bpy.ops.mesh.primitive_cube_add(size=length, location=(-width / 2, length / 2, height))
bpy.ops.mesh.primitive_cube_add(size=width, location=(width / 2, -length / 2, height))
bpy.ops.mesh.primitive_cube_add(size=length, location=(width / 2, length / 2, height))

# Alinear los cubos para formar la estructura
for obj in bpy.context.selected_objects:
    obj.scale = (1, 1, height)

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.handlers['BLEND_OUT'])