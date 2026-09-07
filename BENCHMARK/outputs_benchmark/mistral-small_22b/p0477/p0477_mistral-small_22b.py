import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el terreno con césped
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
terreno = bpy.context.object
terreno.scale = (30, 25, 1)

# Crear el material de césped
material_cesped = bpy.data.materials.new(name="Cesped")
material_cesped.diffuse_color = (0, 1, 0, 1)
terreno.data.materials.append(material_cesped)

# Crear la casa de dos pisos
bpy.ops.mesh.primitive_cube_add(size=1, location=(5, -4, 0))
casa = bpy.context.object
casa.scale = (10, 8, 6)

# Crear el tejado a dos aguas
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=5, depth=3, location=(5, -4, 6))
tejado = bpy.context.object
tejado.rotation_euler = (0, 0, 0.785) # 45 grados

# Crear el árbol
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=3, location=(15, -12, 0))
arbol = bpy.context.object
arbol.scale = (1, 1, 5)

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])