import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
width = 4.0
length = 3.0
height = 2.5

# Crear columnas
for i in range(4):
    x_pos = -width / 2 + (i % 2) * width
    z_pos = height / 2 if i < 2 else -height / 2
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(x_pos, length / 2, z_pos))

# Crear el techo plano
bpy.ops.mesh.primitive_plane_add(size=length + 0.2, location=(0, 0, height))
top_face = bpy.context.object

# Ajustar la escala del techo para que sea más delgado y parezca un techo de madera
top_face.scale = (length, width, 0.1)

# Crear las vigas horizontales
for i in range(4):
    x_pos = -width / 2 + (i % 2) * width
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(x_pos, length / 2, height))
    bpy.ops.transform.resize(value=(length, 0.1, 0))

# Crear las vigas verticales
for i in range(4):
    z_pos = -height / 2 + (i < 2) * height
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-width / 2, length / 2, z_pos))
    bpy.ops.transform.resize(value=(width, length, 0))

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)