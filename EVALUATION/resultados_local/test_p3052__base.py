import bpy

# Crear una nueva escena
bpy.ops.scene.new(name="New Scene")

# Definir propiedades para la vivienda
width = 10
depth = 7
height = 3
room_area = 55

# Crear el suelo
floor = bpy.ops.mesh.primitive_cube_add(size=width * depth, location=(width / 2, depth / 2, height))
floor.scale = (width, depth, 0.1)
floor.name = "Suelo"

# Crear el techo
ceiling = bpy.ops.mesh.primitive_cube_add(size=width * depth, location=(width / 2, depth / 2, height + 0.1))
ceiling.scale = (width, depth, 0.1)
ceiling.name = "Techo"

# Crear el muro exterior
wall_exterior = bpy.ops.mesh.primitive_cube_add(size=width, location=(width / 2, -depth / 2, height))
wall_exterior.scale = (width, depth, height)
wall_exterior.name = "Muro Exterior"

# Crear el muro interior que separa la cocina y el dormitorio
wall_interior = bpy.ops.mesh.primitive_cube_add(size=width, location=(width / 2, depth / 2, height))
wall_interior.scale = (width, depth, height)
wall_interior.name = "Muro Interior"

# Crear el mobiliario esencial
# Sala-comedor y cocina
bpy.ops.mesh.primitive_cube_add(size=width / 2, location=(width / 4, depth / 2, height))
bpy.ops.mesh.primitive_cube_add(size=width / 2, location=(-width / 4, depth / 2, height))

# Dormitorio
bpy.ops.mesh.primitive_cube_add(size=width / 2, location=(width / 2, depth / 2, height))

# Crear el baño
bathroom = bpy.ops.mesh.primitive_cube_add(size=width / 2, location=(width / 2, depth / 2, height))
bathroom.scale = (width / 2, depth / 2, height)

# Crear el mobiliario del baño
bathroom_furniture = bpy.ops.mesh.primitive_cube_add(size=width / 4, location=(width / 4, depth / 4, height))
bathroom_furniture.scale = (width / 4, depth / 4, height)

# Crear el mobiliario del dormitorio
bed = bpy.ops.mesh.primitive_cube_add(size=width / 2, location=(width / 2, depth / 2, height))
bed.scale = (width / 2, depth / 2, height)

# Crear el mobiliario del salón-comedor y cocina
table = bpy.ops.mesh.primitive_cube_add(size=width / 4, location=(width / 4, depth / 2, height))
table.scale = (width / 4, depth / 4, height)

# Ajustar la escala y posicionar correctamente los muebles
for obj in [table, bed]:
    obj.location = (obj.location[0] + width / 8, obj.location[1], obj.location[2])

# Ajustar la escala y posicionar correctamente los muebles del baño
for obj in [bathroom_furniture]:
    obj.location = (obj.location[0] + width / 8, obj.location[1], obj.location[2])

# Ajustar la escala y posicionar correctamente los muebles del dormitorio
for obj in [bed]:
    obj.location = (obj.location[0] + width / 8, obj.location[1], obj.location[2])

# Ajustar la escala y posicionar correctamente los muebles del salón-comedor y cocina
for obj in [table]:
    obj.location = (obj.location[0] + width / 8, obj.location[1], obj.location[2])

# Finalizar la escena
bpy.context.scene.update()