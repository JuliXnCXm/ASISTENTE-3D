import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

altura_poste = 3.0
diametro_poste = 0.1
tamano_cabeza = 0.3

# Crear el poste
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_poste / 2,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste_obj = bpy.context.active_object
poste_obj.name = "PosteLuz"

# Crear la cabeza
bpy.ops.mesh.primitive_cube_add(
    size=tamano_cabeza,
    location=(0, 0, altura_poste - tamano_cabeza / 2)
)
cabeza_obj = bpy.context.active_object
cabeza_obj.name = "CabezaLuz"

# Crear la fuente de luz
bpy.ops.object.light_add(
    type='POINT',
    radius=0.1,
    location=(0, 0, altura_poste - tamano_cabeza / 2)
)
luz_obj = bpy.context.active_object
luz_obj.data.energy = 150 # Watts
luz_obj.name = "FuenteLuz"

# Emparentar objetos
cabeza_obj.parent = poste_obj
luz_obj.parent = poste_obj

# Crear material emisivo para la cabeza
mat_emisivo = bpy.data.materials.new(name="MaterialEmisivo")
mat_emisivo.use_nodes = True
mat_emisivo.node_tree.nodes.remove(mat_emisivo.node_tree.nodes['Principled BSDF'])
shader_node = mat_emisivo.node_tree.nodes.new('ShaderNodeEmission')
shader_node.inputs['Strength'].default_value = 10
output_node = mat_emisivo.node_tree.nodes.get('Material Output')
mat_emisivo.node_tree.links.new(shader_node.outputs['Emission'], output_node.inputs['Surface'])
cabeza_obj.data.materials.append(mat_emisivo)