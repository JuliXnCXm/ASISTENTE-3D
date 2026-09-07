import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del bolardo
altura = 0.9
diametro = 0.3
radio = diametro / 2.0

# Crear el cilindro
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio,
    depth=altura,
    location=(0, 0, 0),
    rotation=(0, 0, 0)
)

# Obtener el objeto recién creado
bolardo = bpy.context.object

# Aplicar un material de hormigón (opcional)
material_name = "Concrete"
material = bpy.data.materials.get(material_name)
if material is None:
    material = bpy.data.materials.new(name=material_name)
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes["Principled BSDF"]
    principled_bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
    principled_bsdf.inputs["Roughness"].default_value = 0.7

bolardo.data.materials.append(material)


# Guardar el archivo .blend (opcional)
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])