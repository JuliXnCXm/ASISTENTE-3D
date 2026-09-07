import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del bolardo
altura = 0.8
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
bolardo = bpy.context.active_object

# Aplicar un material de hormigón (opcional)
material = bpy.data.materials.new(name="Concrete")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.8, 0.6, 0.4, 1)  # Grisáceo
bsdf.inputs["Roughness"].default_value = 0.7
bolardo.data.materials.append(material)


# Guardar el archivo .blend si BLEND_OUT está definido
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])