import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -0.1))
bpy.context.object.scale = (2.0, 1.6, 1)

# Crear los patas de la cama
for x in [-0.8, 0.8]:
    for z in [-0.8, 0.8]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.2, location=(x, 0, z))
        
# Crear el marco de la cama
bpy.ops.mesh.primitive_cube_add(size=0.2, location=(-0.4, 0, -0.4))
bpy.context.object.scale = (1.6, 0.2, 2.0)

# Crear el colchón
bpy.ops.mesh.primitive_plane_add(size=1.8, location=(0, 0, 0.5))
bpy.context.object.scale = (2.0, 1.6, 0.1)
bpy.ops.object.shade_smooth()

# Asignar materiales
material_roble = bpy.data.materials.new(name="Roble")
material_roble.diffuse_color = (0.4, 0.2, 0.05)
for obj in [obj for obj in bpy.context.scene.objects if "cylinder" in obj.name]:
    obj.data.materials.append(material_roble)

material_tela = bpy.data.materials.new(name="Tela")
material_tela.diffuse_color = (1, 1, 1)
bpy.context.object.data.materials.append(material_tela)

# Guardar el archivo si la variable BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)