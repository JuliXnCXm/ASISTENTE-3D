import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de los objetos
sofa_length = 2.5  # metros
sofa_width = 1.8   # metros
mesa_centro_length = 1.2  # metros
mesa_centro_width = 0.6  # metros

# Crea el sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, 0))
obj_sofa = bpy.context.active_object
obj_sofa.name = 'Sofa'

# Aplica la textura de tela gris al sofá
mat_sofa = bpy.data.materials.new(name='TelaGris')
mat_sofa.use_nodes = True
bsdf_sofa = mat_sofa.node_tree.nodes['Principled BSDF']
bsdf_sofa.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1)
obj_sofa.data.materials.append(mat_sofa)

# Crea la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=mesa_centro_length, location=(0, -mesa_centro_width/2, -sofa_length))
obj_mesa_centro = bpy.context.active_object
obj_mesa_centro.name = 'MesaCentro'

# Aplica la textura de madera de nogal a la mesa de centro
mat_mesa_centro = bpy.data.materials.new(name='MaderaNogal')
mat_mesa_centro.use_nodes = True
bsdf_mesa_centro = mat_mesa_centro.node_tree.nodes['Principled BSDF']
bsdf_mesa_centro.inputs['Base Color'].default_value = (0.8, 0.6, 0.4, 1)
obj_mesa_centro.data.materials.append(mat_mesa_centro)

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])