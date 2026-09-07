import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del edificio
width = 15.0  # Ancho en metros
height_per_floor = 3.0  # Altura por piso en metros
total_height = height_per_floor * 3  # Altura total en metros
depth = 0.5  # Profundidad del edificio en metros

# Dimensiones de la ventana
window_width = 1.0
window_height = 1.5
window_depth = 0.1

# Espaciado entre ventanas
window_spacing = 0.5

# Crear el edificio
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, total_height / 2))
building = bpy.context.object
building.scale = (width / 2, depth / 2, total_height / 2)
building.name = "Building"

# Crear ventanas
num_windows_per_row = int((width - window_spacing) / (window_width + window_spacing))
for floor in range(3):
    for i in range(num_windows_per_row):
        x_position = -width / 2 + i * (window_width + window_spacing) + window_width / 2
        z_position = floor * height_per_floor + height_per_floor / 2
        
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x_position, depth / 2, z_position))
        window = bpy.context.object
        window.scale = (window_width / 2, window_depth / 2, window_height / 2)
        window.name = f"Window_Floor_{floor+1}_{i+1}"
        
        # Asignar material a la ventana (opcional)
        # material = bpy.data.materials.new(name="WindowMaterial")
        # material.use_nodes = True
        # bsdf = material.node_tree.nodes["Principled BSDF"]
        # bsdf.inputs["Base Color"].default_value = (0.2, 0.5, 0.8, 1)  # Azul
        # window.data.materials.append(material)

# Crear material para la fachada (opcional)
# material = bpy.data.materials.new(name="FacadeMaterial")
# material.use_nodes = True
# bsdf = material.node_tree.nodes["Principled BSDF"]
# bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)  # Gris claro
# building.data.materials.append(material)

# Guardar el archivo .blend (opcional)
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])