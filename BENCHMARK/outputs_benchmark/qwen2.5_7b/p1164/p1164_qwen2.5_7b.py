import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el piso de parquet
floor = bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -0.1))
bpy.context.object.name = "ParquetFloor"

# Crear la cama de matrimonio (4x2 metros)
bed_length = 4
bed_width = 2
bed = bpy.ops.mesh.primitive_cube_add(size=1, location=(-(bed_length/2-0.5), -(bed_width/2+0.8), -0.1))
bpy.context.object.name = "Bed"
bpy.context.object.scale = (bed_length, bed_width, 1)

# Crear el armario en una esquina (3x1 metros)
cabinet_length = 3
cabinet_width = 1
cabinet_height = 2.5
cabinet = bpy.ops.mesh.primitive_cube_add(size=1, location=(-(bed_length/2-0.5)-1.5, -(bed_width/2+0.8)-0.5, -0.1))
bpy.context.object.name = "Cabinet"
bpy.context.object.scale = (cabinet_length, cabinet_width, cabinet_height)

# Crear las paredes del dormitorio
wall_thickness = 0.1

wall_back = bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
bpy.context.object.name = "WallBack"
bpy.context.object.scale = (bed_length + wall_thickness * 2, bed_width + wall_thickness * 2, wall_thickness)

wall_left = bpy.ops.mesh.primitive_plane_add(size=5, location=(-(bed_length/2-0.5)-1.5 - wall_thickness / 2, -(bed_width/2+0.8) - wall_thickness / 2, 0))
bpy.context.object.name = "WallLeft"
bpy.context.object.scale = (wall_thickness, bed_width + wall_thickness * 2, wall_thickness)

wall_right = bpy.ops.mesh.primitive_plane_add(size=5, location=(bed_length/2-0.5 + bed_length / 2 - wall_thickness / 2, -(bed_width/2+0.8) - wall_thickness / 2, 0))
bpy.context.object.name = "WallRight"
bpy.context.object.scale = (wall_thickness, bed_width + wall_thickness * 2, wall_thickness)

wall_top = bpy.ops.mesh.primitive_plane_add(size=4, location=(-(bed_length/2-0.5), -(bed_width/2+0.8) - wall_thickness / 2, cabinet_height))
bpy.context.object.name = "WallTop"
bpy.context.object.scale = (bed_length + wall_thickness * 2, wall_thickness, wall_thickness)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.background_save_path)