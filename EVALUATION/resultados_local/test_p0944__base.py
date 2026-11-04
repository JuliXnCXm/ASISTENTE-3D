import bpy

# Crear habitación
bpy.ops.mesh.primitive_cube_add(size=6, enter_editmode=False, align='WORLD', location=(0, 0, 0))
bpy.context.object.name = "Habitacion"
bpy.context.object.scale = (6, 4, 2.5)

# Crear mesa rectangular
bpy.ops.mesh.primitive_cube_add(size=1.5, enter_editmode=False, align='WORLD', location=(3, 2, 0.5))
bpy.context.object.name = "Mesa"
bpy.context.object.scale = (3, 1, 0.5)
bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(3, -0.5, 0.5))
bpy.context.object.name = "Silla1"
bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(-3, -0.5, 0.5))
bpy.context.object.name = "Silla2"
bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(-3, 0.5, 0.5))
bpy.context.object.name = "Silla3"
bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(3, 0.5, 0.5))
bpy.context.object.name = "Silla4"
bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(0, 2, 0.5))
bpy.context.object.name = "Silla5"
bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(0, -2, 0.5))
bpy.context.object.name = "Silla6"

# Crear ventana grande
bpy.ops.mesh.primitive_cube_add(size=4, enter_editmode=False, align='WORLD', location=(0, 2, 0.5))
bpy.context.object.name = "Ventana"
bpy.context.object.scale = (4, 2, 0.1)

# Crear lámpara de techo
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 2))
bpy.context.object.name = "Lampara"
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.5, enter_editmode=False, align='WORLD', location=(0, 0, 2.5))
bpy.context.object.name = "LamparaBola"
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.2, enter_editmode=False, align='WORLD', location=(0, 0, 2.7))
bpy.context.object.name = "LamparaPunta"

# Ajustar la escala de la lámpara para que se vea como un área
bpy.context.object.scale = (0.5, 0.5, 0.5)

# Ajustar la escala de la habitación para que se vea adecuada
bpy.context.object.scale = (6, 4, 2.5)

# Ajustar la posición de la lámpara para que esté en el techo
bpy.context.object.location = (0, 0, 2.7)

# Ajustar la posición de la ventana para que esté en la pared larga
bpy.context.object.location = (0, 2, 0.5)

# Ajustar la posición de la mesa para que esté en el centro de la habitación
bpy.context.object.location = (0, 0, 0.5)

# Ajustar la posición de las sillas para que estén alrededor de la mesa
bpy.context.object.location = (-3, -0.5, 0.5)
bpy.context.object.rotation_euler = (0, 0, 0)
bpy.context.object.scale = (0.5, 0.5, 0.5)

bpy.context.object.location = (3, -0.5, 0.5)
bpy.context.object.rotation_euler = (0, 0, 0)
bpy.context.object.scale = (0.5, 0.5, 0.5)

bpy.context.object.location = (3, 0.5, 0.5)
bpy.context.object.rotation_euler = (0, 0, 0)
bpy.context.object.scale = (0.5, 0.5, 0.5)

bpy.context.object.location = (-3, 0.5, 0.5)
bpy.context.object.rotation_euler = (0, 0, 0)
bpy.context.object.scale = (0.5, 0.5, 0.5)

bpy.context.object.location = (0, 2, 0.5)
bpy.context.object.rotation_euler = (0, 0, 0)
bpy.context.object.scale = (0.5, 0.5, 0.5)

bpy.context.object.location = (0, -2, 0.5)
bpy.context.object.rotation_euler = (0, 0, 0)
bpy.context.object.scale = (0.5, 0.5, 0.5)

# Guardar la escena
bpy.ops.wm.save_as_mainfile(filepath="escena_comedor.blend")