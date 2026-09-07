import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el piso de ladrillo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.5))
brick_floor = bpy.context.object
brick_floor.name = "BrickFloor"

# Crear la pared izquierda
bpy.ops.mesh.primitive_plane_add(size=0.2, location=(-4.9, 0, 0.5))
wall_left = bpy.context.object
wall_left.name = "WallLeft"

# Crear la pared derecha
bpy.ops.mesh.primitive_plane_add(size=0.2, location=(4.9, 0, 0.5))
wall_right = bpy.context.object
wall_right.name = "WallRight"

# Crear el muro posterior
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0.5))
back_wall = bpy.context.object
back_wall.name = "BackWall"

# Crear la puerta de entrada centrada
door_width = 2
door_height = 2.4
bpy.ops.mesh.primitive_plane_add(size=door_width, location=(-1, 0, 0.5))
door = bpy.context.object
door.name = "Door"
door.scale = (door_width, door_height, 1)

# Crear las ventanas a cada lado de la puerta
window_width = 1.5
window_height = 2.4
bpy.ops.mesh.primitive_plane_add(size=window_width, location=(-3.75, 0, 0.5))
left_window = bpy.context.object
left_window.name = "LeftWindow"
left_window.scale = (window_width, window_height, 1)

bpy.ops.mesh.primitive_plane_add(size=window_width, location=(3.75, 0, 0.5))
right_window = bpy.context.object
right_window.name = "RightWindow"
right_window.scale = (window_width, window_height, 1)

# Ajustar la escena para que todo esté en el mismo nivel
bpy.ops.object.select_all(action='DESELECT')
brick_floor.select_set(True)
wall_left.select_set(True)
wall_right.select_set(True)
back_wall.select_set(True)
door.select_set(True)
left_window.select_set(True)
right_window.select_set(True)

bpy.context.view_layer.objects.active = brick_floor
bpy.ops.object.join()

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)