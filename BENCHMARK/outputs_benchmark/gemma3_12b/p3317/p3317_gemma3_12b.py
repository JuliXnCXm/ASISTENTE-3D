import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Funciones de utilidad ---
def create_material(name, color, specular=0.1, roughness=0.7):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Specular"].default_value = specular
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

# --- Materiales ---
material_pavement = create_material("PavementMaterial", (0.6, 0.6, 0.6, 1.0))
material_bench = create_material("BenchMaterial", (0.3, 0.3, 0.3, 1.0))
material_lamp = create_material("LampMaterial", (0.8, 0.8, 0.8, 1.0), specular=0.5)
material_tree_trunk = create_material("TreeTrunkMaterial", (0.4, 0.2, 0.1, 1.0))
material_tree_leaves = create_material("TreeLeavesMaterial", (0.2, 0.6, 0.3, 1.0))

# --- Creación de la plaza ---

# Pavimento
pavement_width = 20
pavement_depth = 20
pavement_height = 0.1
bpy.ops.mesh.primitive_plane_add(size=pavement_width, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
pavement = bpy.context.object
pavement.name = "Pavement"
pavement.scale = (pavement_width/2, pavement_depth/2, 1)
pavement.location = (0, 0, pavement_height/2)
pavement.data.materials.append(material_pavement)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Bancas
bench_width = 1.5
bench_depth = 0.5
bench_height = 0.4
bench_count = 4
bench_spacing = pavement_width / (bench_count + 0.5)

for i in range(bench_count):
    x = -pavement_width / 2 + bench_spacing * (i + 0.5)
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x, pavement_depth/2 + 0.2, bench_height/2), scale=(bench_width, bench_depth, bench_height))
    bench = bpy.context.object
    bench.name = "Bench_" + str(i)
    bench.data.materials.append(material_bench)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Farolas
lamp_height = 5
lamp_radius = 0.1
lamp_count = 3
lamp_spacing = pavement_width / (lamp_count + 0.5)

for i in range(lamp_count):
    x = -pavement_width / 2 + lamp_spacing * (i + 0.5)
    bpy.ops.mesh.primitive_cylinder_add(radius=lamp_radius, depth=lamp_height, enter_editmode=False, align='WORLD', location=(x, pavement_depth/2 + 0.2, lamp_height/2), scale=(1, 1, 1))
    lamp = bpy.context.object
    lamp.name = "Lamp_" + str(i)
    lamp.data.materials.append(material_lamp)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Árboles
tree_trunk_height = 0.8
tree_trunk_radius = 0.1
tree_canopy_radius = 0.7
tree_count = 2
tree_spacing = pavement_width / (tree_count + 0.5)

for i in range(tree_count):
    x = -pavement_width / 2 + tree_spacing * (i + 0.5)
    bpy.ops.mesh.primitive_cylinder_add(radius=tree_trunk_radius, depth=tree_trunk_height, enter_editmode=False, align='WORLD', location=(x, pavement_depth/2 + 0.2, tree_trunk_height/2), scale=(1, 1, 1))
    trunk = bpy.context.object
    trunk.name = "TreeTrunk_" + str(i)
    trunk.data.materials.append(material_tree_trunk)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=tree_canopy_radius, enter_editmode=False, align='WORLD', location=(x, pavement_depth/2 + 0.2, tree_trunk_height + tree_canopy_radius), scale=(1, 1, 1))
    canopy = bpy.context.object
    canopy.name = "TreeCanopy_" + str(i)
    canopy.data.materials.append(material_tree_leaves)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# --- Guardar la escena ---
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])