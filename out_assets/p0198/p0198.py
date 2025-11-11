import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

diametro = 0.2
altura = 0.9

bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro / 2,
    depth=altura,
    location=(0, 0, altura / 2),
    vertices=16
)

bolardo_obj = bpy.context.active_object
bolardo_obj.name = "BolardoHormigon"

# Suavizar y añadir material
bpy.ops.object.shade_smooth()
mat = bpy.data.materials.new(name="MaterialHormigonBolardo")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
bolardo_obj.data.materials.append(mat)