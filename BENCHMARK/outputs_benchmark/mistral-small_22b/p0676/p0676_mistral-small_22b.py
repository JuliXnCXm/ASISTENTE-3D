import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
sofa = bpy.context.object
sofa.name = "Sofa"

# Modificar la forma del sofá
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.resize(value=(2, 1, 0.5))
bpy.ops.object.mode_set(mode='OBJECT')

# Crear el material de tela gris para el sofá
material = bpy.data.materials.new(name="Gray Fabric")
material.diffuse_color = (0.5, 0.5, 0.5)
sofa.data.materials.append(material)

# Crear la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0, -0.7))
table = bpy.context.object
table.name = "Table"

# Modificar la forma de la mesa
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.resize(value=(1, 0.5, 0.2))
bpy.ops.object.mode_set(mode='OBJECT')

# Crear el material de madera de roble para la mesa
material = bpy.data.materials.new(name="Oak Wood")
material.diffuse_color = (0.8, 0.4, 0.2)
table.data.materials.append(material)

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])