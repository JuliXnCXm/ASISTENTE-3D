import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del muro
largo_muro = 10.0
alto_muro = 2.2
grosor_muro = 0.2

# Dimensiones de la puerta
ancho_puerta = 1.0
alto_puerta = 2.0
grosor_puerta = 0.1

# Crear el muro de ladrillo
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, alto_muro/2), scale=(1, 1, 1))
muro = bpy.context.object
muro.name = "Muro"
muro.scale = (largo_muro/2, 0.5, alto_muro/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -grosor_muro)})
bpy.ops.object.mode_set(mode='OBJECT')

# Crear la puerta de madera
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, alto_puerta/2), scale=(1, 1, 1))
puerta = bpy.context.object
puerta.name = "Puerta"
puerta.scale = (ancho_puerta/2, 0.5, alto_puerta/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -grosor_puerta)})
bpy.ops.object.mode_set(mode='OBJECT')

# Posicionar la puerta en el muro
posicion_puerta_x = (largo_muro / 2) - (ancho_puerta / 2)
puerta.location = (posicion_puerta_x, 0, alto_puerta/2)

# Crear el material de ladrillo
material_ladrillo = bpy.data.materials.new(name="Ladrillo")
material_ladrillo.use_nodes = True
principled_bsdf = material_ladrillo.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.8, 0.3, 0.1, 1)
principled_bsdf.inputs["Roughness"].default_value = 0.6
muro.data.materials.append(material_ladrillo)

# Crear el material de madera
material_madera = bpy.data.materials.new(name="Madera")
material_madera.use_nodes = True
principled_bsdf_madera = material_madera.node_tree.nodes["Principled BSDF"]
principled_bsdf_madera.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1)
principled_bsdf_madera.inputs["Roughness"].default_value = 0.4
puerta.data.materials.append(material_madera)

# Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])