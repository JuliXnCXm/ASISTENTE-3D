import bpy

# Crear una nueva escena
bpy.ops.scene.new(name="Casa")

# Definir las dimensiones de la casa
width = 8
length = 10
height = 3 # Altura total de la casa (2 pisos + techo)

# Crear el suelo
bpy.ops.mesh.primitive_cube_add(size=width*length, location=(0, 0, -height/2))
cube = bpy.context.object
cube.name = "Suelo"
cube.scale = (width, length, height)
cube.rotation_euler = (0, 0, 0)

# Crear el tejado
bpy.ops.mesh.primitive_cube_add(size=width*length, location=(0, 0, height/2))
tejado = bpy.context.object
tejado.name = "Tejado"
tejado.scale = (width, length, height)
tejado.rotation_euler = (0, 0, 0)

# Crear la fachada frontal
fachada = bpy.ops.mesh.primitive_cube_add(size=length, location=(width/2, 0, height/2))
fachada = bpy.context.object
fachada.name = "Fachada"
fachada.scale = (width, length, height)
fachada.rotation_euler = (0, 0, 0)

# Crear la puerta principal
bpy.ops.mesh.primitive_cube_add(size=1, location=(width/2-0.5, 0, height/2+1))
puerta = bpy.context.object
puerta.name = "Puerta"
puerta.scale = (1, 2, 2)
puerta.rotation_euler = (0, 0, 0)

# Crear las ventanas
for i in range(4):
    ventana = bpy.ops.mesh.primitive_cube_add(size=1, location=(width/2-0.5, i*2, height/2+1))
    ventana = bpy.context.object
    ventana.name = "Ventana"
    ventana.scale = (1, 1, 2)
    ventana.rotation_euler = (0, 0, 0)

# Ajustar la escala para que se vea bien
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = '/tmp/casa.png'

# Guardar el archivo
bpy.ops.wm.save_as_mainfile(filepath='/tmp/casa.blend')