import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
width = 1.6
length = 2.0
height = 0.1

# Crear el colchón de textil blanco
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.05))
colchon = bpy.context.object
colchon.scale = (width / 2, length / 2, height)
colchon.name = "Colchon"
colchon.data.name = "Colchon"

# Asignar material al colchón
material = bpy.data.materials.new(name="Blanco")
material.diffuse_color = (1, 1, 1, 1)
colchon.data.materials.append(material)

# Crear la estructura de madera de nogal
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, -0.15))
estructura = bpy.context.object
estructura.scale = (width / 2 + 0.05, length / 2 + 0.05, height)
estructura.name = "Estructura"
estructura.data.name = "Estructura"

# Asignar material a la estructura
material_madera = bpy.data.materials.new(name="Nogal")
material_madera.diffuse_color = (0.627, 0.419, 0.258, 1)
estructura.data.materials.append(material_madera)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)