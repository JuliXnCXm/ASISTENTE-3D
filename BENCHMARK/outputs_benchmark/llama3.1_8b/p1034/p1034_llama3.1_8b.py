import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la cama
ancho = 1.6
largo = 2.0

# Crea el marco de madera
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, 0, 0))
marco = bpy.context.active_object
marco.name = "Marco"

# Ajusta las dimensiones del marco para que coincida con la cama
marco.scale = (ancho, largo, 0.1)

# Crea los pies de la cama
bpy.ops.mesh.primitive_cube_add(size=0.2, location=(-ancho/2, -largo/2, 0))
pie_izquierdo = bpy.context.active_object
pie_izquierdo.name = "Pie Izquierdo"

bpy.ops.mesh.primitive_cube_add(size=0.2, location=(ancho/2, -largo/2, 0))
pie_derecho = bpy.context.active_object
pie_derecho.name = "Pie Derecho"

# Ajusta las dimensiones de los pies para que coincida con la cama
pie_izquierdo.scale = (0.2, 0.2, 0.1)
pie_derecho.scale = (0.2, 0.2, 0.1)

# Crea el colchón
bpy.ops.mesh.primitive_plane_add(size=ancho, location=(0, 0, 0))
colchon = bpy.context.active_object
colchon.name = "Colchon"

# Ajusta las dimensiones del colchón para que coincida con la cama
colchon.scale = (ancho, largo, 0.1)

# Crea el tejido del colchón
bpy.ops.mesh.primitive_plane_add(size=ancho, location=(0, 0, 0))
tejido = bpy.context.active_object
tejido.name = "Tejido"

# Ajusta las dimensiones del tejido para que coincida con la cama
tejido.scale = (ancho, largo, 0.1)

# Coloca el colchón sobre el marco
colchon.location = (0, 0, 0.05)
marco.location = (0, 0, -0.05)

# Coloca los pies de la cama en su lugar
pie_izquierdo.location = (-ancho/2, -largo/2, -0.05)
pie_derecho.location = (ancho/2, -largo/2, -0.05)

# Guarda el archivo .blend si se especificó la ruta de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])