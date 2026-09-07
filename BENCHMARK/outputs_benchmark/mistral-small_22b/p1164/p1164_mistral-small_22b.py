import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del dormitorio
width = 4
depth = 5
height = 2.5

# Crear el suelo de parquet
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, height / 2))
floor = bpy.context.object
floor.scale.x = width
floor.scale.y = depth
floor.name = "Floor"

# Crear la cama de matrimonio
bpy.ops.mesh.primitive_cube_add(size=1, location=(depth / 2 - 0.5, 0.5, height / 4))
bed = bpy.context.object
bed.scale.x = 2  # Ancho de la cama
bed.scale.y = 0.1  # Altura de la cama
bed.scale.z = 1  # Profundidad de la cama
bed.name = "Bed"

# Crear el armario en una esquina
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, 0.5, height / 4))
wardrobe = bpy.context.object
wardrobe.scale.x = 1  # Ancho del armario
wardrobe.scale.y = 2  # Altura del armario
wardrobe.scale.z = 0.5  # Profundidad del armario
wardrobe.name = "Wardrobe"

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])