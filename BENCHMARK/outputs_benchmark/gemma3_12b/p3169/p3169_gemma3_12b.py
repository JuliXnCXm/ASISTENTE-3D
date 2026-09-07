import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la oficina
office_width = 8
office_depth = 6
office_height = 2.8

# Dimensiones de la sala de reuniones
meeting_width = 3
meeting_depth = 4

# Dimensiones del tabique de vidrio
glass_wall_thickness = 0.1

# Dimensiones del escritorio
desk_width = 1.2
desk_depth = 0.8
desk_height = 0.74

# Dimensiones de la silla ergonómica
chair_width = 0.6
chair_depth = 0.6
chair_height = 0.9

# Dimensiones de la cajonera
drawer_width = 0.45
drawer_depth = 0.5
drawer_height = 0.6

# Dimensiones de la mesa de reuniones
meeting_table_width = 1.5
meeting_table_depth = 2.4
meeting_table_height = 0.74

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=office_width, enter_editmode=False, align='WORLD', location=(office_width/2, office_depth/2, 0))
floor = bpy.context.object
floor.name = "Floor"
floor.scale = (1, office_depth/office_width, 1)

# Crear las paredes
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(office_width/2, office_depth/2, office_height/2))
wall_front = bpy.context.object
wall_front.name = "FrontWall"
wall_front.scale = (office_width/2, office_depth/2, office_height/2)
wall_front.location = (0, office_depth/2, office_height/2)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(office_width/2, office_depth/2, office_height/2))
wall_back = bpy.context.object
wall_back.name = "BackWall"
wall_back.scale = (office_width/2, office_depth/2, office_height/2)
wall_back.location = (0, -office_depth/2, office_height/2)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(office_width/2, office_depth/2, office_height/2))
wall_left = bpy.context.object
wall_left.name = "LeftWall"
wall_left.scale = (office_width/2, office_depth/2, office_height/2)
wall_left.location = (-office_width/2, office_depth/2, office_height/2)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(office_width/2, office_depth/2, office_height/2))
wall_right = bpy.context.object
wall_right.name = "RightWall"
wall_right.scale = (office_width/2, office_depth/2, office_height/2)
wall_right.location = (office_width/2, -office_depth/2, office_height/2)

# Crear el tabique de vidrio
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(office_width/2, office_depth/2, office_height/2))
glass_wall = bpy.context.object
glass_wall.name = "GlassWall"
glass_wall.scale = (meeting_width/2, glass_wall_thickness/2, office_height/2)
glass_wall.location = (office_width - meeting_width/2, office_depth/2, office_height/2)

# Crear los puestos de trabajo (4)
for i in range(4):
    # Escritorio
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    desk = bpy.context.object
    desk.name = f"Desk_{i}"
    desk.scale = (desk_width/2, desk_depth/2, desk_height/2)
    desk.location = (office_width/2 - (desk_width + 0.2) * (i % 2), office_depth/2 - (desk_width + 0.2) * (i // 2), desk_height/2)

    # Silla
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    chair = bpy.context.object
    chair.name = f"Chair_{i}"
    chair.scale = (chair_width/2, chair_depth/2, chair_height/2)
    chair.location = (desk.location.x + chair_width/2, desk.location.y - chair_depth/2, chair_height/2)

    # Cajonera
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    drawer = bpy.context.object
    drawer.name = f"Drawer_{i}"
    drawer.scale = (drawer_width/2, drawer_depth/2, drawer_height/2)
    drawer.location = (desk.location.x - drawer_width/2, desk.location.y - drawer_depth/2, drawer_height/2)

# Crear la mesa de reuniones
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
meeting_table = bpy.context.object
meeting_table.name = "MeetingTable"
meeting_table.scale = (meeting_table_width/2, meeting_table_depth/2, meeting_table_height/2)
meeting_table.location = (office_width - meeting_width/2, office_depth/2, meeting_table_height/2)

# Crear las sillas de la sala de reuniones (6)
for i in range(6):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    meeting_chair = bpy.context.object
    meeting_chair.name = f"MeetingChair_{i}"
    meeting_chair.scale = (chair_width/2, chair_depth/2, chair_height/2)
    meeting_chair.location = (meeting_table.location.x + (chair_width + 0.2) * (i % 3), meeting_table.location.y - (chair_depth + 0.2) * (i // 3), chair_height/2)

# Guardar el archivo
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])