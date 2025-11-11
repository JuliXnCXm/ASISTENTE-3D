import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 5.0
alto = 2.5
espesor = 0.2

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo / 2, espesor / 2, alto / 2),
    scale=(largo, espesor, alto)
)

wall_obj = bpy.context.active_object
wall_obj.name = "MuroLadrillo"

mat = bpy.data.materials.new(name="MaterialLadrillo")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.1, 0.05, 1)
wall_obj.data.materials.append(mat)