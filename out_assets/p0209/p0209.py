import bpy

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

largo = 3.0
ancho = 1.5
alto = 2.4
grosor = 0.1

# Pared trasera
bpy.ops.mesh.primitive_cube_add(location=(0, -ancho/2 + grosor/2, alto/2))
pared = bpy.context.object
pared.scale = (largo/2, grosor/2, alto/2)
bpy.ops.object.transform_apply(scale=True)

# Techo
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto - grosor/2))
techo = bpy.context.object
techo.scale = (largo/2, ancho/2, grosor/2)
bpy.ops.object.transform_apply(scale=True)

# Panel lateral de vidrio
grosor_vidrio = 0.02
bpy.ops.mesh.primitive_cube_add(location=(-largo/2 + grosor/2, 0, alto/2))
vidrio = bpy.context.object
vidrio.scale = (grosor/2, ancho/2, alto/2)
bpy.ops.object.transform_apply(scale=True)

# Material de vidrio con Glass BSDF
mat_vidrio = bpy.data.materials.new(name="GlassMaterial")
mat_vidrio.use_nodes = True
nt = mat_vidrio.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new('ShaderNodeOutputMaterial')
glass = nt.nodes.new('ShaderNodeBsdfGlass')
glass.inputs['IOR'].default_value = 1.45
glass.inputs['Roughness'].default_value = 0.1
nt.links.new(glass.outputs['BSDF'], out.inputs['Surface'])

vidrio.data.materials.append(mat_vidrio)
