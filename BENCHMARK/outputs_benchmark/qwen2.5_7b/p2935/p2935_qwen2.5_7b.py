import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define los materiales
wood_material = bpy.data.materials.new(name="Wood")
concrete_material = bpy.data.materials.new(name="Concrete")

# Asigna los materiales a las geometrías
wood_material.diffuse_color = (0.5, 0.23, 0.14, 1)
concrete_material.diffuse_color = (0.2, 0.2, 0.2, 1)

# Crea la losa de hormigón
bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0, 0, -0.075))
losa = bpy.context.object
losa.scale = (4.0, 3.0, 0.15)
losa.data.materials.append(concrete_material)

# Crea los postes verticales
for x in [-2.0, 2.0]:
    for z in [-1.5, 1.5]:
        bpy.ops.mesh.primitive_cube_add(size=0.15, location=(x, 0, z + 2.5))
        poste = bpy.context.object
        poste.scale = (0.15, 0.15, 2.5)
        poste.data.materials.append(wood_material)

# Crea las vigas horizontales
for x in [-2.0, 2.0]:
    bpy.ops.mesh.primitive_cube_add(size=0.3, location=(x, 0, 2.5))
    viga = bpy.context.object
    viga.scale = (0.3, 0.15, 0)
    viga.data.materials.append(wood_material)

for z in [-1.5, 1.5]:
    bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0, 0, z + 2.5))
    viga = bpy.context.object
    viga.scale = (0.15, 0.3, 0)
    viga.data.materials.append(wood_material)

# Guarda el archivo si la variable de entorno BLEND_OUT existe
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)