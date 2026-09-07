import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del dormitorio en metros
room_width = 4
room_depth = 5
room_height = 2.5

# Crear el dormitorio
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, room_height/2), scale=(room_width, room_depth, room_height))
room = bpy.context.object
room.name = "Room"

# Crear el piso de parquet
parquet_width = 0.1
parquet_depth = 0.1
parquet_height = 0.05

for x in range(int(room_width / parquet_width)):
    for y in range(int(room_depth / parquet_depth)):
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x * parquet_width, y * parquet_depth, 0), scale=(parquet_width, parquet_depth, parquet_height))
        parquet = bpy.context.object
        parquet.name = f"Parquet_{x}_{y}"

# Crear la cama
bed_width = 1.6
bed_depth = 2.0
bed_height = 0.5

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(room_width/2 - bed_width/2, room_depth/2 - bed_depth/2, bed_height/2), scale=(bed_width, bed_depth, bed_height))
bed = bpy.context.object
bed.name = "Bed"

# Crear el armario
wardrobe_width = 1.2
wardrobe_depth = 0.6
wardrobe_height = 2.0

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, room_depth - wardrobe_depth, wardrobe_height/2), scale=(wardrobe_width, wardrobe_depth, wardrobe_height))
wardrobe = bpy.context.object
wardrobe.name = "Wardrobe"

# Opcional: Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    filepath = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=filepath)