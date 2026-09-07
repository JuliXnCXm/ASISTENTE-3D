import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo del jardín
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, -1))

# Crear las columnas de la pérgola
column_locations = [
    (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)
]
for loc in column_locations:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=3, location=loc)

# Crear el techo plano ligero de la pérgola
bpy.ops.mesh.primitive_plane_add(size=(4, 3), location=(0, 0, 1))

# Guardar el archivo .blend si existe BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])