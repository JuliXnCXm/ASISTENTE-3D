import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

altura_poste = 4.0
radio_poste = 0.15 / 2
tamano_luminaria = 0.3

# Poste
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "PosteFarola"

# Luminaria
bpy.ops.mesh.primitive_cube_add(
    size=tamano_luminaria,
    location=(0, 0, altura_poste + tamano_luminaria / 2)
)
luminaria = bpy.context.active_object
luminaria.name = "Luminaria"

# Material emisivo (sin sockets de Principled)
mat_emisivo = bpy.data.materials.new(name="LuzFarola")
mat_emisivo.use_nodes = True
nt = mat_emisivo.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new('ShaderNodeOutputMaterial')
emi = nt.nodes.new('ShaderNodeEmission')
emi.inputs['Color'].default_value = (1.0, 0.8, 0.4, 1.0)
emi.inputs['Strength'].default_value = 15.0
nt.links.new(emi.outputs['Emission'], out.inputs['Surface'])

luminaria.data.materials.append(mat_emisivo)
