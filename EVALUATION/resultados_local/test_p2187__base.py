import bpy

# Crear una estructura de acero
bpy.ops.mesh.primitive_cube_add(size=10)
acero = bpy.context.object
acero.name = "EstructuraAcero"
acero.location = (0, 0, 5)

# Crear un banco de hormigón
bpy.ops.mesh.primitive_cube_add(size=2)
banco = bpy.context.object
banco.name = "BancoHormigon"
banco.location = (0, -3, 0)

# Crear un techo de vidrio curvado
bpy.ops.mesh.primitive_cube_add(size=10)
techo = bpy.context.object
techo.name = "TechoVidrio"
techo.location = (0, 0, 0)
techo.rotation_euler = (0, 0, math.pi/2) # Curva el techo
techo.scale = (10, 10, 10)

# Agregar costillas metálicas al techo
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=1)
    costilla = bpy.context.object
    costilla.name = f"Costilla{i}"
    costilla.location = (i*2.5, 0, 0)
    costilla.rotation_euler = (0, math.pi/4, 0)
    costilla.scale = (1, 1, 1)

# Ajustar la escala para que todo encaje correctamente
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 100