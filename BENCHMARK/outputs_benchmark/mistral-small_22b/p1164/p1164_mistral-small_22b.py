import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el dormitorio
wall_length = 4
wall_width = 5
floor_height = 0.1

# Piso de parquet
bpy.ops.mesh.primitive_plane_add(size=1, location=(wall_length / 2, wall_width / 2, floor_height))
parquet = bpy.context.active_object
parquet.name = "Parquet"

# Cama de matrimonio
bed_length = 2
bed_width = 1.5
bed_height = 0.5
bpy.ops.mesh.primitive_cube_add(size=bed_length, location=(wall_length - bed_length - 0.5, wall_width / 2 - bed_width / 2, bed_height))
bed = bpy.context.active_object
bed.name = "Cama"

# Armario en una esquina
wardrobe_length = 1
wardrobe_width = 0.5
wardrobe_depth = 0.5
bpy.ops.mesh.primitive_cube_add(size=wardrobe_length, location=(wall_length - wardrobe_length - 0.5, wardrobe_width / 2 + 0.1, wardrobe_depth / 2))
wardrobe = bpy.context.active_object
wardrobe.name = "Armario"

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])