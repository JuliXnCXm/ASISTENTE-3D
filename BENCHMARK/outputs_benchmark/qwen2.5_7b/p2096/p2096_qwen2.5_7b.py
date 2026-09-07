import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.5))

# Cama con cabecero tapizado
bpy.ops.mesh.primitive_cube_add(size=2, location=(-3, 0, 0))
bpy.ops.transform.resize(value=(2, 2, 0.1))
bpy.context.object.name = "Cama"

# Cabecero de la cama
bpy.ops.mesh.primitive_cube_add(size=1, location=(-3, 0, 1.5))
bpy.ops.transform.resize(value=(1, 1, 0.2))
bpy.context.object.name = "Cabecero_Cama"

# Tapizado del cabecero (usando un material simple)
material = bpy.data.materials.new(name="Tapizado")
material.diffuse_color = (0.5, 0.2, 0.8, 1)
bpy.context.object.data.materials.append(material)

# Muro bajo separador para vestidor
bpy.ops.mesh.primitive_cube_add(size=4, location=(3, 0, -0.5))
bpy.ops.transform.resize(value=(4, 0.2, 2))
bpy.context.object.name = "Muro_Bajo_Vestidor"

# Armarios empotrados
for i in range(2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(3 + (i * 1), -1, 0.5))
    bpy.ops.transform.resize(value=(1, 2, 2.5))
    bpy.context.object.name = f"Armario_Empotrado_{i}"

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.background_save_path)