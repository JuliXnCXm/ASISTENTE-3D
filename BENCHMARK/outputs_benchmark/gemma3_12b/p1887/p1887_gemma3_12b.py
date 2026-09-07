import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Funciones de utilidad ---
def create_mesh(name, vertices, edges, faces):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

def set_location(obj, x, y, z):
    obj.location = (x, y, z)

def set_rotation(obj, x, y, z):
    obj.rotation_euler = (math.radians(x), math.radians(y), math.radians(z))

# --- Escritorio en forma de L ---
def create_l_desk(width1, depth1, width2, depth2, height):
    vertices = [
        (0, 0, 0),
        (width1, 0, 0),
        (width1, depth1, 0),
        (0, depth1, 0),
        (0, 0, height),
        (width1, 0, height),
        (width1, depth1, height),
        (0, depth1, height),
    ]
    edges = []
    faces = [
        (0, 1, 2, 3),  # Base
        (4, 5, 6, 7),  # Top
        (0, 1, 2, 3, 4, 3, 0), # Side 1
        (1, 2, 3, 4, 5, 3, 1), # Side 2
        (2, 3, 4, 5, 6, 4, 2), # Side 3
        (3, 0, 1, 2, 6, 5, 4) # Side 4
    ]

    desk = create_mesh("L_Desk", vertices, edges, faces)
    set_location(desk, 0, 0, height)
    return desk

# --- Silla de oficina ---
def create_office_chair(width, depth, height, back_height):
    vertices = [
        (0, 0, 0),
        (width, 0, 0),
        (width, depth, 0),
        (0, depth, 0),
        (width/2, depth/2, height),
        (0, 0, height),
        (width, 0, height),
        (width, depth, height),
        (0, depth, height),
    ]
    edges = []
    faces = [
        (0, 1, 2, 3),
        (4, 0, 1, 5),
        (5, 1, 2, 6),
        (6, 2, 3, 7),
        (7, 3, 0, 4),
    ]

    chair = create_mesh("Office_Chair", vertices, edges, faces)
    set_location(chair, 0, 0, 0)
    return chair

# --- Estantería de pared paramétrica ---
def create_parametric_bookshelf(width, depth, height, num_shelves, shelf_spacing):
    shelves = []
    for i in range(num_shelves):
        z_pos = i * shelf_spacing
        vertices = [
            (0, 0, z_pos),
            (width, 0, z_pos),
            (width, depth, z_pos),
            (0, depth, z_pos),
        ]
        faces = [(0, 1, 2, 3)]
        shelf = create_mesh(f"Shelf_{i}", vertices, [], faces)
        set_location(shelf, 0, 0, z_pos)
        shelves.append(shelf)
    return shelves

# --- Parámetros ---
desk_width1 = 1.5
desk_depth1 = 0.8
desk_width2 = 1.2
desk_depth2 = 0.6
desk_height = 0.75

chair_width = 0.6
chair_depth = 50
chair_height = 0.45
back_height = 0.6

bookshelf_width = 1.0
bookshelf_depth = 0.3
bookshelf_height = 0.8
num_shelves = 4
shelf_spacing = 0.2

# --- Creación de objetos ---
desk = create_l_desk(desk_width1, desk_depth1, desk_width2, desk_depth2, desk_height)
chair = create_office_chair(chair_width, chair_depth, chair_height, back_height)
set_location(chair, 0.5, 0.5, 0)
bookshelves = create_parametric_bookshelf(bookshelf_width, bookshelf_depth, bookshelf_height, num_shelves, shelf_spacing)
for shelf in bookshelves:
    set_location(shelf, 1.5, 0, 0)

# --- Modificadores (Opcional) ---
# Ejemplo: Agregar un modificador de subdivisión a la mesa
# desk.modifiers.new(name="Subdivision", type='SUBSURF')
# desk.modifiers["Subdivision"].levels = 2
# desk.modifiers["Subdivision"].render_levels = 2

# --- Guardar la escena (Opcional) ---
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])