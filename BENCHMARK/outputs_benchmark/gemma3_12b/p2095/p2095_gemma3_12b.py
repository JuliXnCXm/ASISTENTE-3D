import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Funciones de utilidad ---
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color + (1,)  #RGBA
    return mat

def set_origin_to_geometry(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# --- Materiales ---
mat_sofa = create_material("SofaMat", (0.2, 0.2, 0.2)) # Gris oscuro
mat_carpet = create_material("CarpetMat", (0.8, 0.7, 0.5)) # Beige
mat_bookshelf = create_material("BookshelfMat", (0.9, 0.9, 0.9)) # Gris claro

# --- Sala de estar ---
# Dimensiones de la sala
room_width = 6
room_depth = 8
room_height = 2.5

# Crear suelo
bpy.ops.mesh.primitive_plane_add(size=room_width, enter_editmode=False, align='WORLD', location=(0, 0, 0))
room_floor = bpy.context.object
room_floor.scale = (1, room_depth/room_width, 1)
room_floor.location = (0, 0, 0)
room_floor.data.materials.append(mat_carpet)

# --- Sofá modular ---
sofa_module_width = 1
sofa_module_depth = 0.8
sofa_module_height = 0.7

# Crear módulo del sofá
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
sofa_module = bpy.context.object
sofa_module.scale = (sofa_module_width, sofa_module_depth, sofa_module_height)
sofa_module.data.materials.append(mat_sofa)

# Crear el sofá modular (3 módulos)
sofa_modules = []
for i in range(3):
    new_module = sofa_module.copy()
    new_module.data = sofa_module.data.copy()
    new_module.name = f"SofaModule_{i}"
    bpy.context.collection.objects.link(new_module)
    new_module.location = (i * sofa_module_width * 1.2, 0, 0)
    sofa_modules.append(new_module)

# --- Alfombra ---
carpet_width = 3
carpet_depth = 4
carpet_thickness = 0.2

bpy.ops.mesh.primitive_plane_add(size=carpet_width, enter_editmode=False, align='WORLD', location=(0, 0, 0))
carpet = bpy.context.object
carpet.scale = (1, carpet_depth/carpet_width, 1)
carpet.location = (0, 0, 0.01)
carpet.data.materials.append(mat_carpet)

# --- Estantería de diseño irregular ---
bookshelf_width = 2
bookshelf_depth = 0.3
bookshelf_height = 1.5

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
bookshelf = bpy.context.object
bookshelf.scale = (bookshelf_width, bookshelf_depth, bookshelf_height)
bookshelf.data.materials.append(mat_bookshelf)
bookshelf.location = (0, -bookshelf_depth, bookshelf_height/2)

# Modificador de subdivisiones
subdivision_modifier = bookshelf.modifiers.new(name="Subdivision", type='SUBSURF')
subdivision_modifier.levels = 3
subdivision_modifier.render_levels = 3

# Modificador de deformación por calor
heat_deformation_modifier = bookshelf.modifiers.new(name="HeatDeform", type='HEAT')
heat_deformation_modifier.angle = 20
heat_deformation_modifier.distance = 0.2
heat_deformation_modifier.noise_scale = 1.0

# --- Ajustes finales ---
for obj in [sofa_module, bookshelf]:
    set_origin_to_geometry(obj)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])