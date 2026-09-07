import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea un plano para el tejado a dos aguas
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 3))

# Selecciona el plano y lo renombramos
obj = bpy.context.active_object
obj.name = "Tejado"

# Aplicamos una transformación para darle la forma de un tejado a dos aguas
bpy.ops.object.mode_set(mode='EDIT')
verts = obj.data.vertices

# Calcula los vértices del tejado a dos aguas
for i in range(len(verts)):
    v = verts[i].co
    if i == 0:
        verts[i].co = mathutils.Vector((v.x, v.y + 2, v.z))
    elif i == 1:
        verts[i].co = mathutils.Vector((v.x, v.y - 2, v.z))
    else:
        verts[i].co = mathutils.Vector((v.x, v.y, v.z))

# Aplicamos la transformación
bpy.ops.object.mode_set(mode='OBJECT')

# Aplica una textura para darle color al tejado
obj.active_material = bpy.data.materials.new(name="TejadoMaterial")
mat = obj.active_material
mat.use_nodes = True

# Selecciona el nodo de color y lo cambia a gris claro
node_tree = mat.node_tree.nodes
node_color = node_tree.nodes.get('Principled BSDF')
node_color.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])