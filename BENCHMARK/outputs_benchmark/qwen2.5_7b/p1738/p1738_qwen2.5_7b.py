import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir el radio de la copa del árbol
radius = 2.0

# Definir la altura total del árbol (copa + tronco)
total_height = 4.0 + 2.5

# Crear el tronco del árbol
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=2.5, location=(0, 0, total_height / 2 - 2.5 / 2))

# Crear la copa del árbol
bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, total_height / 2 + radius))
bpy.ops.transform.resize(value=(1, 1, (total_height / 2 - radius) / radius))

# Alinear la copa con el tronco
for obj in bpy.context.selected_objects:
    obj.location = (0, 0, total_height / 2)

# Guardar el archivo blend si existe BLEND_OUT en las variables de entorno
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)