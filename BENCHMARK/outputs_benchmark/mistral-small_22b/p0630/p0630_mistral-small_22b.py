import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el sofá
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
sofa = bpy.context.object
sofa.scale = (3, 1, 1)

# Añade un material gris para el sofá
material = bpy.data.materials.new(name="GrayMaterial")
material.diffuse_color = (0.5, 0.5, 0.5, 1)
sofa.data.materials.append(material)

# Crea la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(2, 0, 0))
table = bpy.context.object
table.scale = (1, 1, 0.1)

# Añade un material de madera para la mesa
material = bpy.data.materials.new(name="WoodMaterial")
material.diffuse_color = (0.8, 0.4, 0.2, 1)
table.data.materials.append(material)

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])