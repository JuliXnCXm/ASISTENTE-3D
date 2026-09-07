import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el colchón
colchon = bpy.data.objects.new("Colchon", None)
colchon.location = (0, 0, 0.5)
bpy.ops.object.transform_apply(scale=False)
bpy.context.view_layer.objects.active = colchon
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
colchon.data.name = "Colchon"
colchon.scale = (1, 2, 0.5)

# Crear la estructura de madera
madera = bpy.data.objects.new("Madera", None)
madera.location = (0, 0, -0.5)
bpy.ops.object.transform_apply(scale=False)
bpy.context.view_layer.objects.active = madera
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
madera.data.name = "Madera"
madera.scale = (1, 2, 0.5)

# Asignar materiales
material_blanco = bpy.data.materials.new(name="MaterialBlanco")
material_blanco.diffuse_color = (1, 1, 1, 1)
colchon.data.materials.append(material_blanco)

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])