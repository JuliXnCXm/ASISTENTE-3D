import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Funciones de utilidad ---
def create_material(name, color, specular=0.5, roughness=0.5):
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
material_pavement = create_material("PavementMaterial", (0.6, 0.6, 0.6, 1.0), specular=0.1, roughness=0.8)
material_bench = create_material("BenchMaterial", (0.3, 0.3, 0.3, 1.0), specular=0.2, roughness=0.6)
material_lamp = create_material("LampMaterial", (0.8, 0.8, 0.8, 1.0), specular=0.7, roughness=0.2)
material_tree_trunk = create_material("TreeTrunkMaterial", (0.4, 0.2, 0.1, 1.0), specular=0.1, roughness=0.9)
material_tree_leaves = create_material("TreeLeavesMaterial", (0.2, 0.6, 0.2, 1.0), specular=0.1, roughness=0.7)

# --- Dimensiones generales ---
square_size = 20  # Metros
raised_bed_size = 3  # Metros
raised_bed_height = 0.3 # Metros
tree_height = 5 # Metros
lamp_height = 8 # Metros

# --- Pavimento ---
bpy.ops.mesh.primitive_plane_add(size=square_size, enter_editmode=False, align='WORLD', location=(0, 0, 0))
plane = bpy.context.object
plane.name = "Pavement"
plane.data.materials.append(material_pavement)

# --- Alcorque elevado ---
bpy.ops.mesh.primitive_cube_add(size=raised_bed_size, enter_editmode=False, align='WORLD', location=(0, 0, raised_bed_height/2))
raised_bed = bpy.context.object
raised_bed.name = "RaisedBed"
raised_bed.data.materials.append(material_pavement)

# --- Árbol ---
# Tronco
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=tree_height, enter_editmode=False, align='WORLD', location=(0, 0, tree_height/2))
tree_trunk = bpy.context.object
tree_trunk.name = "TreeTrunk"
tree_trunk.data.materials.append(material_tree_trunk)

# Hojas (esfera simplificada)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, enter_editmode=False, align='WORLD', location=(0, 0, tree_height))
tree_leaves = bpy.context.object
tree_leaves.name = "TreeLeaves"
tree_leaves.data.materials.append(material_tree_leaves)

# --- Bancas (rectángulos) ---
bench_width = 0.4
bench_depth = 0.5
bench_height = 0.45

# Banca 1
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(-square_size/2 + 1, -square_size/2 + 1, bench_height/2))
bench1 = bpy.context.object
bench1.name = "Bench1"
bench1.scale = (bench_depth, bench_width, bench_height)
bench1.data.materials.append(material_bench)

# Banca 2
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(square_size/2 - 1, square_size/2 - 1, bench_height/2))
bench2 = bpy.context.object
bench2.name = "Bench2"
bench2.scale = (bench_depth, bench_width, bench_height)
bench2.data.materials.append(material_bench)

# --- Farolas (cilindros) ---
lamp_radius = 0.15
bpy.ops.mesh.primitive_cylinder_add(radius=lamp_radius, depth=lamp_height, enter_editmode=False, align='WORLD', location=(0, square_size/2, lamp_height/2))
lamp1 = bpy.context.object
lamp1.name = "Lamp1"
lamp1.data.materials.append(material_lamp)

bpy.ops.mesh.primitive_cylinder_add(radius=lamp_radius, depth=lamp_height, enter_editmode=False, align='WORLD', location=(0, -square_size/2, lamp_height/2))
lamp2 = bpy.context.object
lamp2.name = "Lamp2"
lamp2.data.materials.append(material_lamp)

# --- Opcional: Guardar el archivo ---
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])