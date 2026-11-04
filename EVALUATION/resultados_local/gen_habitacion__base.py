import bpy

# Crear el espacio del dormitorio
bpy.ops.mesh.primitive_cube_add(size=4, enter_editmode=False, align='WORLD', location=(0, 0, 0))
dormitorio = bpy.context.object
dormitorio.name = "Dormitorio"
dormitorio.scale = (4, 3.5, 2.5) # Altura de 2.5 metros

# Crear la cama doble
bpy.ops.mesh.primitive_cube_add(size=1.8, enter_editmode=False, align='WORLD', location=(1.6, 1.75, 0.5))
cama = bpy.context.object
cama.name = "Cama"
cama.scale = (1.8, 1.8, 0.5)

# Crear el armario
bpy.ops.mesh.primitive_cube_add(size=1.5, enter_editmode=False, align='WORLD', location=(-1.5, 1.75, 0.5))
armario = bpy.context.object
armario.name = "Armario"
armario.scale = (1.5, 1.5, 2)

# Crear la ventana
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(1.9, 1.75, 2.25))
ventana = bpy.context.object
ventana.name = "Ventana"
ventana.scale = (1, 1, 1)