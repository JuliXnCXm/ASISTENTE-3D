import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el terreno de césped
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
terreno = bpy.context.object
terreno.name = "Terreno"

# Añade un material para el césped
material_cesped = bpy.data.materials.new(name="Cesped")
material_cesped.diffuse_color = (0, 1, 0)
terreno.data.materials.append(material_cesped)

# Crea el árbol
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3, location=(2, 2, 0))
arbol = bpy.context.object
arbol.name = "Arbol"

# Añade un material para el tronco del árbol
material_tronco = bpy.data.materials.new(name="Tronco")
material_tronco.diffuse_color = (0.5, 0.3, 0)
arbol.data.materials.append(material_tronco)

# Crea las hojas del árbol
bpy.ops.mesh.primitive_cone_add(radius1=2, radius2=0, depth=1, location=(2, 2, 3))
hojas = bpy.context.object
hojas.name = "Hojas"

# Añade un material para las hojas del árbol
material_hojas = bpy.data.materials.new(name="Hojas")
material_hojas.diffuse_color = (0, 1, 0)
hojas.data.materials.append(material_hojas)

# Crea el banco de madera
bpy.ops.mesh.primitive_cube_add(size=2, location=(4, 0, 0))
banco = bpy.context.object
banco.name = "Banco"

# Añade un material para el banco de madera
material_madera = bpy.data.materials.new(name="Madera")
material_madera.diffuse_color = (0.8, 0.4, 0)
banco.data.materials.append(material_madera)

# Guarda el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])