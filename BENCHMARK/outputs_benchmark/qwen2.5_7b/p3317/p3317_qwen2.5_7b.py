import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir los materiales
pavimento_material = bpy.data.materials.new(name="Pavimento")
pavimento_material.diffuse_color = (0.4, 0.35, 0.3, 1)
bancas_material = bpy.data.materials.new(name="Bancas")
bancas_material.diffuse_color = (0.8, 0.7, 0.6, 1)
farolas_material = bpy.data.materials.new(name="Farolas")
farolas_material.diffuse_color = (0.95, 0.9, 0.85, 1)
arbol_material = bpy.data.materials.new(name="Arboles")
arbol_material.diffuse_color = (0.3, 0.2, 0.1, 1)

# Crear el pavimento
pavimento = bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, -0.1))
bpy.context.object.data.materials.append(pavimento_material)

# Crear las bancas
for i in range(-20, 21, 5):
    for j in range(-20, 21, 5):
        banco = bpy.ops.mesh.primitive_cube_add(size=3, location=(i, j, -0.4))
        banco_obj = bpy.context.object
        banco_obj.data.materials.append(bancas_material)

# Crear las farolas
for i in range(-20, 21, 7):
    for j in range(-20, 21, 7):
        farola = bpy.ops.mesh.primitive_cube_add(size=1.5, location=(i, j, 3))
        farola_obj = bpy.context.object
        farola_obj.data.materials.append(farolas_material)

# Crear los árboles
for i in range(-20, 21, 10):
    arbol = bpy.ops.mesh.primitive_cube_add(size=1.5, location=(i, -23, 0))
    arbol_obj = bpy.context.object
    arbol_obj.data.materials.append(arbol_material)

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)