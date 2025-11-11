import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

ancho_x = 10.0
profundo_y = 10.0
espesor_z = 0.3

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -espesor_z / 2),
    scale=(ancho_x, profundo_y, espesor_z)
)

slab_obj = bpy.context.active_object
slab_obj.name = "LosaHormigon"

mat = bpy.data.materials.new(name="MaterialHormigon")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1)
mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.8
slab_obj.data.materials.append(mat)