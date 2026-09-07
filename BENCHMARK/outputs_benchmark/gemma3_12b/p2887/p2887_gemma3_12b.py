import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del bolardo
height = 0.9
diameter = 0.3
radius = diameter / 2.0

# Crear el bolardo (cilindro)
bpy.ops.mesh.primitive_cylinder_add(
    radius=radius,
    depth=height,
    location=(0, 0, 0),
    rotation=(0, 0, 0)
)

# Obtener el objeto recién creado
bolardo = bpy.context.active_object

# Aplicar un material de hormigón (opcional)
material = bpy.data.materials.new(name="Concrete")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
bsdf.inputs["Roughness"].default_value = 0.7
bolardo.data.materials.append(material)


# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)