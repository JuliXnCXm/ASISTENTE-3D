import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear un cilindro para representar el bolardo
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.9, location=(0, 0, 0))

# Renombrar la mesh al objeto "bolardo"
obj = bpy.context.object
obj.name = "bolardo"

# Ajustar el material (opcional)
mat = bpy.data.materials.new(name="Hormigón")
mat.diffuse_color = (0.451, 0.227, 0.098, 1)  # Color de hormigón
obj.data.materials.append(mat)

# Guardar el archivo blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene[BLEND_OUT])