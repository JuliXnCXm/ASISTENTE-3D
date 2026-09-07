import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las proporciones de la vivienda
ancho = 10  # metros
fondo = 5   # metros
alto = 3.5  # metros

# Crea el suelo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -alto))
bpy.context.object.name = "Suelo"
bpy.context.object.scale = (ancho, fondo, alto)

# Crea la pared delantera
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2, 0, 0))
bpy.context.object.name = "Pared_Delante"
bpy.context.object.scale = (ancho, alto, alto)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi / 2, 0, 0))

# Crea la pared trasera
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2, 0, 0))
bpy.context.object.name = "Pared_Trasera"
bpy.context.object.scale = (ancho, alto, alto)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi / 2, 0, 0))

# Crea la pared izquierda
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -fondo/2, 0))
bpy.context.object.name = "Pared_Izquierda"
bpy.context.object.scale = (alto, fondo, alto)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi / 2, 0, 0))

# Crea la pared derecha
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, fondo/2, 0))
bpy.context.object.name = "Pared_Derecha"
bpy.context.object.scale = (alto, fondo, alto)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi / 2, 0, 0))

# Crea el techo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -alto))
bpy.context.object.name = "Techo"
bpy.context.object.scale = (ancho, fondo, alto)

# Guarda la escena si se especificó un archivo de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])