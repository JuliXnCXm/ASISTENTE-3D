import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -0.1))
bpy.context.object.scale = (2.0, 1.6, 1.0)  # Ajustar al tamaño de la cama

# Crear las estructuras laterales
for side in [(-0.8, 0), (-0.8, 1.6)]:
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(side[0], side[1] / 2, -0.05))
    bpy.context.object.scale = (0.1, 1.6, 0.1)
    
for end in [(0, -0.8), (0, 0.8)]:
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(end[0] / 2, end[1], -0.05))
    bpy.context.object.scale = (1.6, 0.1, 0.1)

# Crear el marco superior
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, 0.2))
bpy.context.object.scale = (1.6, 1.6, 0.1)

# Crear el colchón
bpy.ops.mesh.primitive_plane_add(size=1.8, location=(0, 0, 0.15))
bpy.context.object.scale = (2.0, 1.6, 0.05)  # Ajustar al tamaño del colchón

# Cambiar el material de la cama a nogal
for obj in bpy.context.scene.objects:
    if "Cube" in obj.name or "Plane" in obj.name:
        mat = bpy.data.materials.new(name="Nogal")
        mat.diffuse_color = (0.6, 0.45, 0.2)
        obj.data.materials.append(mat)

# Cambiar el material del colchón a blanco
for obj in bpy.context.scene.objects:
    if "colchon" in obj.name:
        mat = bpy.data.materials.new(name="Blanco")
        mat.diffuse_color = (1, 1, 1)
        obj.data.materials.append(mat)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)