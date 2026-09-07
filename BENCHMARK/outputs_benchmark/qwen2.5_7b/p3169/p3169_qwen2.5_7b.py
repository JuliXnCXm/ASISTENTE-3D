import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el piso y las paredes principales
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
bpy.ops.transform.resize(value=(8, 6, 1))

# Altura del techo
bpy.ops.object.modifier_add(type='SOLIDIFY')
bpy.context.object.modifiers["Solidify"].thickness = 2.8

# Crear los puestos de trabajo
for i in range(4):
    x_pos = -3 + (i % 2) * 1.5
    y_pos = 1.5 - (i // 2) * 1.5
    bpy.ops.mesh.primitive_cube_add(size=0.8, location=(x_pos, y_pos, 0))
    
    # Escritorio
    desk = bpy.context.object.copy()
    desk.location = (x_pos, y_pos, 0.3)
    bpy.context.collection.objects.link(desk)
    
    # Silla ergonómica
    chair = bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1, location=(x_pos, y_pos + 0.4, 0.7))
    bpy.context.object.name = "Chair_" + str(i)
    
    # Cajonera
    drawer = bpy.ops.mesh.primitive_cube_add(size=0.6, location=(x_pos - 0.25, y_pos - 0.15, 0.3))

# Crear el tabique de vidrio para la sala de reuniones
bpy.ops.mesh.primitive_plane_add(size=7, location=(-4.5, 1.5, 2.8))
bpy.ops.transform.resize(value=(3, 4, 1))
bpy.ops.object.modifier_add(type='SOLIDIFY')
bpy.context.object.modifiers["Solidify"].thickness = 0.1

# Crear la mesa para la sala de reuniones
table = bpy.ops.mesh.primitive_cube_add(size=2, location=(-3.5, -1.5, 2))
bpy.context.object.name = "Table"

# Amueblar la sala de reuniones con sillas
for i in range(6):
    x_pos = -3 + (i % 3) * 0.8
    y_pos = -1.4 - (i // 3) * 0.8
    chair = bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1, location=(x_pos, y_pos, 1.7))
    bpy.context.object.name = "Chair_" + str(i + 4)

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)