import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
width = 1.6
length = 2.0
thickness = 0.05

# Crear el marco de madera
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
cama = bpy.context.object
cama.scale = (width / 2, length / 2, thickness)

# Crear las barras laterales y pies
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-width/4, -length/2, -thickness/2))
lateral_izquierdo = bpy.context.object
lateral_izquierdo.scale = (0.1, length / 2, thickness)

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(width/4, -length/2, -thickness/2))
lateral_derecho = bpy.context.object
lateral_derecho.scale = (0.1, length / 2, thickness)

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-width/2, -length/2, -thickness/2))
pie_izquierdo = bpy.context.object
pie_izquierdo.scale = (width / 4, 0.1, thickness)

bpy.ops.mesh.primitive_cube_add(size=0.1, location=(width/2, -length/2, -thickness/2))
pie_derecho = bpy.context.object
pie_derecho.scale = (width / 4, 0.1, thickness)

# Crear el colchón de textil blanco
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -thickness - 0.05))
colchon = bpy.context.object
colchon.scale = (width / 2, length / 2, 0.1)
colchon.color = (1, 1, 1, 1)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)