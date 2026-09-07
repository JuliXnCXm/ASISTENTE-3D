import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades de la geometría
nogal = {
    'nombre': 'Nogal',
    'color': (0.5, 0.2, 0.1),
    'dureza': 10,
}

tela = {
    'nombre': 'Tela Blanca',
    'color': (1, 1, 1),
    'transparencia': 0.5,
}

# Crea el marco de la cama
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cama = bpy.context.active_object

# Aplica materiales a los objetos
mat_nogal = bpy.data.materials.new(name=nogal['nombre'])
mat_nogal.diffuse_color = nogal['color']
mat_nogal.specular_intensity = 0.5
bpy.ops.object.select_all(action='DESELECT')
cama.select_set(True)
bpy.context.view_layer.objects.active = cama
cama.data.materials.append(mat_nogal)

# Crea los pies de la cama
bpy.ops.mesh.primitive_cube_add(size=1, location=(-1.5, 0, -2))
pie_derecho = bpy.context.active_object
mat_nogal.copy()
pie_derecho.data.materials.append(mat_nogal)
pie_derecho.location = (-1.5, 0, -2)

bpy.ops.mesh.primitive_cube_add(size=1, location=(1.5, 0, -2))
pie_izquierdo = bpy.context.active_object
mat_nogal.copy()
pie_izquierdo.data.materials.append(mat_nogal)
pie_izquierdo.location = (1.5, 0, -2)

# Crea el colchón de tela blanca
bpy.ops.mesh.primitive_plane_add(size=3, location=(0, 0, 0))
colchon = bpy.context.active_object

mat_tela = bpy.data.materials.new(name=tela['nombre'])
mat_tela.diffuse_color = tela['color']
mat_tela.specular_intensity = 0.5
mat_tela.use_nodes = True
bsdf_node = mat_tela.node_tree.nodes.get('Principled BSDF')
bsdf_node.inputs['Base Color'].default_value = (1, 1, 1, 1)
bsdf_node.inputs['Metallic'].default_value = 0.5

colchon.data.materials.append(mat_tela)

# Guarda el archivo .blend si se especificó la ruta
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene.BLEND_OUT)