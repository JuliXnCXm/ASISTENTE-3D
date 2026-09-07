import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del bolardo
diametro = 0.2
altura = 0.9

# Crear el cilindro
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro / 2,
    depth=altura,
    location=(0, 0, altura / 2),
    rotation=(0, 0, 0)
)

# Obtener el objeto recién creado
bolardo = bpy.context.object

# Aplicar un material de hormigón (opcional)
material = bpy.data.materials.new(name="Concrete")
material.use_nodes = True
principled_bsdf = material.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
principled_bsdf.inputs["Roughness"].default_value = 0.7
bolardo.data.materials.append(material)


# Guardar el archivo .blend si BLEND_OUT está definido
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])