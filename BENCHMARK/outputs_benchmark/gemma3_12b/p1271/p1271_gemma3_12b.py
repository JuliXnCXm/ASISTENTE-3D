import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Funciones de utilidad ---
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color + (1,)  # A, R, G, B
    return mat

# --- Materiales ---
material_grass = create_material("GrassMaterial", (0.2, 0.5, 0.3))
material_roof = create_material("RoofMaterial", (0.8, 0.3, 0.1))
material_wall = create_material("WallMaterial", (0.9, 0.9, 0.9))
material_tree_trunk = create_material("TrunkMaterial", (0.4, 0.2, 0.1))
material_tree_leaves = create_material("LeavesMaterial", (0.1, 0.6, 0.1))


# --- Terreno de césped ---
bpy.ops.mesh.primitive_plane_add(size=25, enter_editmode=False, align='WORLD', location=(0, 0, 0))
grass_plane = bpy.context.object
grass_plane.scale = (1, 1, 1)
grass_plane.data.materials.clear()
grass_plane.data.materials.append(material_grass)


# --- Casa de campo ---
house_width = 12
house_depth = 9
house_height = 2.5

# Paredes
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, house_height/2))
house_wall = bpy.context.object
house_wall.scale = (house_width/2, house_depth/2, house_height/2)
house_wall.data.materials.clear()
house_wall.data.materials.append(material_wall)

# Tejado a dos aguas
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, house_height + 1))
roof_plane = bpy.context.object
roof_plane.scale = (house_width/2, house_depth, 1)
roof_plane.rotation_euler[0] = math.radians(45)
roof_plane.data.materials.clear()
roof_plane.data.materials.append(material_roof)

# --- Árbol ---
tree_location = ( -6, -5, 0)
tree_trunk_height = 2
tree_trunk_radius = 0.2

# Tronco del árbol
bpy.ops.mesh.primitive_cylinder_add(radius=tree_trunk_radius, depth=tree_trunk_height, enter_editmode=False, align='WORLD', location=tree_location + (0, 0, tree_trunk_height/2))
tree_trunk = bpy.context.object
tree_trunk.data.materials.clear()
tree_trunk.data.materials.append(material_tree_trunk)

# Hojas del árbol
leaves_radius = 3
leaves_location = (0, 0, tree_trunk_height + leaves_radius * 0.75)
bpy.ops.mesh.primitive_uv_sphere_add(radius=leaves_radius, enter_editmode=False, align='WORLD', location=tree_location + leaves_location)
tree_leaves = bpy.context.object
tree_leaves.data.materials.clear()
tree_leaves.data.materials.append(material_tree_leaves)


# --- Guardar el archivo .blend (opcional) ---
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])