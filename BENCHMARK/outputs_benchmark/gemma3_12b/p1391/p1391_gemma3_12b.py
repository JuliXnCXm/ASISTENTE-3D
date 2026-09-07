import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la parcela de tierra
parcel_size = 5

# Crear la parcela de tierra
bpy.ops.mesh.primitive_plane_add(size=parcel_size, enter_editmode=False, align='WORLD', location=(0, 0, 0))
ground = bpy.context.object
ground.name = "Ground"
ground.data.name = "GroundData"

# Crear la copa del árbol
bpy.ops.mesh.primitive_uv_sphere_add(radius=3, enter_editmode=False, align='WORLD', location=(0, 0, 3))
tree_canopy = bpy.context.object
tree_canopy.name = "TreeCanopy"
tree_canopy.data.name = "TreeCanopyData"

# Subdividir la copa del árbol para suavizarla
bpy.ops.object.shade_smooth()
bpy.ops.object.modifier_add(type='SUBSURF')
tree_canopy.modifiers["Subdivision"].levels = 3
bpy.ops.object.modifier_apply(modifier="Subdivision")

# Crear el tronco del árbol (cilindro)
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 1))
tree_trunk = bpy.context.object
tree_trunk.name = "TreeTrunk"
tree_trunk.data.name = "TreeTrunkData"

# Suavizar el tronco
bpy.ops.object.shade_smooth()

# Aplicar un material simple al tronco
material_trunk = bpy.data.materials.new(name="TrunkMaterial")
material_trunk.use_nodes = True
bsdf = material_trunk.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.6, 0.3, 0.1, 1)  # Marrón
tree_trunk.data.materials.append(material_trunk)

# Aplicar un material simple a la copa del árbol
material_canopy = bpy.data.materials.new(name="CanopyMaterial")
material_canopy.use_nodes = True
bsdf_canopy = material_canopy.node_tree.nodes["Principled BSDF"]
bsdf_canopy.inputs["Base Color"].default_value = (0.1, 0.5, 0.1, 1)  # Verde
tree_canopy.data.materials.append(material_canopy)

# Opcional: Guardar el archivo .blend
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])