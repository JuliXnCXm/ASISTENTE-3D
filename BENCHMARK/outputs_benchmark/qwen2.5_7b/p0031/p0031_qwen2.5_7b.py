import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones y el espesor
length = 6.0
width = 4.0
thickness = 0.20

# Crea un plano rectangular para la losa de piso
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
floor = bpy.context.object

# Escala el plano a las dimensiones deseadas
floor.scale = (length, width, thickness)

# Mueve la losa de piso al centro del origen
floor.location = (length / 2, width / 2, thickness / 2)

# Guarda el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in bpy.context.scene:
    blend_out_path = bpy.context.scene[BLEND_OUT]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)