import bpy

# Limpia la escena
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
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
casa = bpy.context.object
casa.scale = (10, 8, 4)

# Crear el tejado a dos aguas
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=5, depth=2, location=(0, 0, 4))
tejado = bpy.context.object
tejado.rotation_euler = (0, 0, 0.785)  # 45 grados

# Crear el árbol
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=3, location=(15, -12, 0))
arbol = bpy.context.object
arbol.scale = (1, 1, 1)

# Crear el material del tronco del árbol
material_tronco = bpy.data.materials.new(name="Tronco")
material_tronco.diffuse_color = (0.5, 0.35, 0.05, 1)
arbol.data.materials.append(material_tronco)

# Crear el material de las hojas del árbol
material_hojas = bpy.data.materials.new(name="Hojas")
material_hojas.diffuse_color = (0, 1, 0, 1)

# Añadir materiales al árbol
arbol.data.materials[0].name = "Tronco"
arbol.data.materials.append(material_hojas)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])