import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear suelo de porcelanato (planta abierta 8x6 metros)
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.1))
suelo = bpy.context.object
suelo.scale = (8, 6, 1)

# Zona de estar
bpy.ops.mesh.primitive_cylinder_add(radius=2, depth=0.5, location=(-3, 2, 0.25))
sofá = bpy.context.object
sofá.scale = (2, 1, 1)

bpy.ops.mesh.primitive_cube_add(size=1, location=(-3, 1, 1))
estantería = bpy.context.object
estantería.scale = (4, 0.5, 1)

# Zona de comedor
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=0.5, location=(2, -2, 0.25))
mesa = bpy.context.object
mesa.scale = (3, 1.5, 1)

for i in range(4):
    silla_radius = 0.5 + i * 0.2
    bpy.ops.mesh.primitive_cylinder_add(radius=silla_radius, depth=0.8, location=(2 + i * 0.6 - 1, -3, 0.7))
    
# Luz de área en el techo
bpy.ops.object.lightprobe_add(
    location=(0, 0, 5), 
    rotation=(1.5708, 0, 1.5708)
)
luz_area = bpy.context.object
luz_area.scale = (2, 2, 2)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.properties.BLEND_OUT)