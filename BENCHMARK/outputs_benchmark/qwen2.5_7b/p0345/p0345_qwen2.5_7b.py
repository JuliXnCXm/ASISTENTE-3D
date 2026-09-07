import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las propiedades de los materiales
hormigon_material = bpy.data.materials.new(name="Hormigón")
hormigon_material.diffuse_color = (0.4, 0.2, 0.1, 1)
baranda_material = bpy.data.materials.new(name="Baranda Metálica")
baranda_material.diffuse_color = (0.8, 0.7, 0.6, 1)

# Asignar materiales a los objetos
hormigon_material.use_nodes = True
baranda_material.use_nodes = True

# Crear la escalera
escalera = bpy.ops.mesh.primitive_cube_add(location=(0, -3, 0))
bpy.context.object.scale = (0.5, 0.1, 2)  # Ancho, Profundidad, Altura
for i in range(14):
    new_cube = escalera()
    new_cube.location = (0, -3 + 0.1 * (i + 1), 2 * (i + 1))
bpy.ops.object.shade_smooth()

# Crear la baranda en el descanso superior
baranda = bpy.ops.mesh.primitive_cube_add(location=(0, -3 + 0.1 * 15, 30))
baranda_scale = (4, 0.2, 0.2)
baranda_location = (0, -3 + 0.1 * 15, 30)
bpy.context.object.scale = baranda_scale
bpy.ops.transform.translate(value=baranda_location)

# Asignar materiales a los objetos
escalera_obj = bpy.context.object
baranda_obj = bpy.context.object

escalera_obj.data.materials.append(hormigon_material)
baranda_obj.data.materials.append(baranda_material)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)