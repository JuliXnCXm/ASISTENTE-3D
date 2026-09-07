import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del terreno
ancho = 15
alto = 10

# Crea un plano para el terreno
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))

# Selecciona el plano creado
objeto = bpy.context.active_object

# Establece las dimensiones del plano
objeto.dimensions = (ancho, alto, 0.01)

# Renombra el objeto a "Terreno"
bpy.ops.object.rename(object=objeto, new_name='Terreno')

# Aplica un material de césped al terreno
mat_cespillo = bpy.data.materials.new(name="Cesped")
mat_cespillo.use_nodes = True

# Obtiene la escena actual
scene = bpy.context.scene

# Establece el color del material
mat_cespillo.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.3, 0.6, 0.2, 1)

# Aplica el material al objeto
objeto.data.materials.append(mat_cespillo)

# Guarda la escena si se especificó un archivo de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])