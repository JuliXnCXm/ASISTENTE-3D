import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de los objetos
sofa_length = 2.5  # metros
sofa_width = 1.8   # metros
mesa_centro_length = 0.9  # metros
mesa_centro_width = 0.6   # metros

# Crea el plano para el sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, 0))
obj_sofa = bpy.context.active_object
obj_sofa.name = 'Sofa'

# Aplica la textura de tela gris al sofá
mat_sofa = bpy.data.materials.new(name='TelaGris')
mat_sofa.use_nodes = True
bsdf = mat_sofa.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1)
obj_sofa.data.materials.append(mat_sofa)

# Crea el plano para la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=mesa_centro_length, location=(0, -mesa_centro_width/2, -sofa_length))
obj_mesa_centro = bpy.context.active_object
obj_mesa_centro.name = 'MesaCentro'

# Aplica la textura de madera al sofá y mesa de centro
mat_madera = bpy.data.materials.new(name='MaderaNogal')
mat_madera.use_nodes = True
bsdf = mat_madera.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.8, 0.6, 0.4, 1)
obj_sofa.data.materials.append(mat_madera)
obj_mesa_centro.data.materials.append(mat_madera)

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])