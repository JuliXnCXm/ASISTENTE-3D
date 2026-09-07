import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del terreno
ancho = 15
alto = 15

# Crea un plano para el terreno
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))

# Selecciona el plano creado
objeto = bpy.context.active_object
objeto.name = 'Terreno'

# Aplica una textura de césped al objeto
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.object.mode_set(mode='EDIT')

# Crea un nuevo material para la textura de césped
material = bpy.data.materials.new(name='Césped')
material.use_nodes = True

# Obtiene el nodo de color del material
principio = material.node_tree.nodes['Principio']
principio.inputs[0].default_value = (0.5, 1, 0.5, 1)  # Verde claro para el césped

# Aplica la textura al objeto
objeto.data.materials.append(material)

# Escala el terreno a las dimensiones deseadas
bpy.ops.transform.resize(value=(ancho, alto, 0))

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend con ese nombre
if 'BLEND_OUT' in os.environ:
    bpy.context.blend_file.use_save_dirty = True
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])