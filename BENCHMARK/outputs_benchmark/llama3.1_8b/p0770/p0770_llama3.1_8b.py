import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del objeto en metros
sofa_length = 2.5
sofa_width = 1.8
mesa_centro_length = 1.5
mesa_centro_width = 0.8

# Crea el sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -1.5, 0))
obj_sofo = bpy.context.active_object
obj_sofo.name = 'Sofa'
obj_sofo.scale = (sofa_width, sofa_length, 0.8)

# Crea la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=mesa_centro_length, location=(0, -2.5, 1))
obj_mesa_centro = bpy.context.active_object
obj_mesa_centro.name = 'Mesa Centro'
obj_mesa_centro.scale = (mesa_centro_width, mesa_centro_length, 0.8)

# Aplica la textura al sofá y a la mesa de centro
mat_sofo = bpy.data.materials.new(name='SofaMaterial')
mat_sofo.use_nodes = True
bsdf_node = mat_sofo.node_tree.nodes['Principled BSDF']
bsdf_node.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1)
obj_sofo.data.materials.append(mat_sofo)

mat_mesa_centro = bpy.data.materials.new(name='MesaCentroMaterial')
mat_mesa_centro.use_nodes = True
bsdf_node = mat_mesa_centro.node_tree.nodes['Principled BSDF']
bsdf_node.inputs['Base Color'].default_value = (0.8, 0.6, 0.4, 1)
obj_mesa_centro.data.materials.append(mat_mesa_centro)

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])