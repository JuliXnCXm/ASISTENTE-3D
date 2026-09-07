import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del muro
length = 10.0  # Longitud del muro en metros
height = 2.5   # Altura del muro en metros
thickness = 0.2  # Espesor del muro en metros

# Crear el muro perimetral
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.1))
wall = bpy.context.object
wall.scale = (length, height, thickness)

# Definir las dimensiones de la apertura para el portón
door_width = 3.0  # Ancho del portón en metros

# Crear la apertura en el centro del muro
door_location = (length / 2 - door_width / 2, 0, height / 2)
bpy.ops.mesh.primitive_cube_add(size=1, location=door_location)
door = bpy.context.object
door.scale = (door_width, height, thickness)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)