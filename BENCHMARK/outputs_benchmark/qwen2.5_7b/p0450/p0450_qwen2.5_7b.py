import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el cuerpo de la cama (estructura de madera)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.5))
cama = bpy.context.object

# Ajustar el tamaño y la posición
cama.scale = (2, 1, 1)  # Ancho: 2m, Profundidad: 1m, Altura: 1m
bpy.ops.transform.translate(value=(0, -0.5, 0))  # Centrar en el eje Y

# Crear el colchón (cubo blanco)
colchon = bpy.data.objects.new(name="Colchon", object_data=bpy.data.meshes.new("Colchon"))
bpy.context.collection.objects.link(colchon)
colchon.scale = (1.8, 0.9, 0.2)  # Ancho: 1.8m, Profundidad: 0.9m, Altura: 0.2m
bpy.ops.transform.translate(value=(0, -0.45, 0.6))  # Centrar en el eje Y y ajustar altura

# Asignar material al colchón (blanco)
material = bpy.data.materials.new(name="Blanco")
material.diffuse_color = (1, 1, 1, 1)  # Color blanco
colchon.data.materials.append(material)

# Seleccionar y actualizar la escena
bpy.context.view_layer.objects.active = cama
bpy.ops.object.select_all(action='DESELECT')
cama.select_set(True)
bpy.context.view_layer.update()

if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])