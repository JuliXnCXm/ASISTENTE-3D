import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del muro
longitud_muro = 8.0
altura_muro = 2.2
grosor_muro = 0.2
ancho_puerta = 1.0

# Crear el muro de ladrillo
bpy.ops.mesh.primitive_plane_add(size=1.0, enter_editmode=False, align='WORLD', location=(0, 0, altura_muro/2), scale=(1, 1, 1))
muro = bpy.context.object
muro.name = "Muro"
muro.scale[0] = longitud_muro
muro.scale[1] = grosor_muro
muro.scale[2] = 1.0

# Subdividir el muro para crear la textura de ladrillo (opcional)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=10)
bpy.ops.object.mode_set(mode='OBJECT')

# Crear la puerta
bpy.ops.mesh.primitive_plane_add(size=1.0, enter_editmode=False, align='WORLD', location=(0, 0, 2.2/2), scale=(1, 1, 1))
puerta = bpy.context.object
puerta.name = "Puerta"
puerta.scale[0] = 1.0
puerta.scale[1] = 0.1
puerta.scale[2] = 1.0
puerta.location[0] = longitud_muro/2 - ancho_puerta/2
puerta.location[2] = altura_muro/2

# Crear material para el muro (ladrillo)
material_ladrillo = bpy.data.materials.new(name="Ladrillo")
material_ladrillo.use_nodes = True
principled_bsdf = material_ladrillo.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.8, 0.3, 0.1, 1)
principled_bsdf.inputs["Roughness"].default_value = 0.6
muro.data.materials.append(material_ladrillo)

# Crear material para la puerta (madera)
material_madera = bpy.data.materials.new(name="Madera")
material_madera.use_nodes = True
principled_bsdf_madera = material_madera.node_tree.nodes["Principled BSDF"]
principled_bsdf_madera.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1)
principled_bsdf_madera.inputs["Roughness"].default_value = 0.8
puerta.data.materials.append(material_madera)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])