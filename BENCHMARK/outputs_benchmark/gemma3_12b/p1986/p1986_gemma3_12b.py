import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Funciones de utilidad ---
def create_material(name, color, specular=0.5, roughness=0.3):
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

def assign_material(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# --- Materiales ---
material_quartz = create_material("Quartz", (0.9, 0.9, 0.9, 1.0), specular=0.6, roughness=0.1)
material_cabinet = create_material("Cabinet", (0.2, 0.2, 0.2, 1.0), specular=0.1, roughness=0.8)
material_steel = create_material("Steel", (0.1, 0.1, 0.1, 1.0), specular=0.9, roughness=0.05)
material_wood = create_material("Wood", (0.6, 0.4, 0.2, 1.0), specular=0.1, roughness=0.7)

# --- Dimensiones (en metros) ---
cabinet_width = 1.5
cabinet_height = 0.9
cabinet_depth = 0.6
island_width = 3.0
island_length = 2.0
island_height = 0.9
countertop_thickness = 0.03
hood_width = 1.2
hood_length = 0.6
hood_height = 0.4

# --- Gabinetes ---
# Gabinete 1
bpy.ops.mesh.primitive_cube_add(size=cabinet_width, location=(0, 0, cabinet_height/2))
cabinet1 = bpy.context.object
cabinet1.scale = (1, cabinet_depth/cabinet_width, cabinet_height/cabinet_width)
assign_material(cabinet1, material_cabinet)

# Gabinete 2
bpy.ops.mesh.primitive_cube_add(size=cabinet_width, location=(cabinet_width, 0, cabinet_height/2))
cabinet2 = bpy.context.object
cabinet2.scale = (1, cabinet_depth/cabinet_width, cabinet_height/cabinet_width)
assign_material(cabinet2, material_cabinet)

# Gabinete 3
bpy.ops.mesh.primitive_cube_add(size=cabinet_width, location=(2*cabinet_width, 0, cabinet_height/2))
cabinet3 = bpy.context.object
cabinet3.scale = (1, cabinet_depth/cabinet_width, cabinet_height/cabinet_width)
assign_material(cabinet3, material_cabinet)

# --- Isla Central ---
bpy.ops.mesh.primitive_cube_add(size=island_width, location=(island_width/2, island_length/2, island_height/2))
island = bpy.context.object
island.scale = (1, 1, 1)
assign_material(island, material_quartz)

# --- Encimera de la Isla ---
bpy.ops.mesh.primitive_cube_add(size=island_width, location=(island_width/2, island_length/2, 0))
countertop = bpy.context.object
countertop.scale = (1, 1, countertop_thickness)
assign_material(countertop, material_quartz)

# --- Campana Extractora ---
bpy.ops.mesh.primitive_cube_add(size=hood_width, location=(island_width/2, island_length/2 + hood_length/2, island_height + hood_height/2))
hood = bpy.context.object
hood.scale = (1, 1, 1)
assign_material(hood, material_steel)

# --- Encimera de los Gabinetes ---
bpy.ops.mesh.primitive_cube_add(size=island_width + 3*cabinet_width, location=(island_width/2 + 1.5*cabinet_width, island_length/2, 0))
countertop_main = bpy.context.object
countertop_main.scale = (1, 1, countertop_thickness)
assign_material(countertop_main, material_quartz)

# --- Ajustes finales ---
bpy.context.view_layer.update()

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])