import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear un bolardo cilíndrico
radius = 0.15  # Radio (mitad del diámetro)
height = 0.8   # Altura

# Crear una esfera y ajustar su tamaño para formar un cilindro
bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, location=(0, 0, 0))

# Seleccionar el objeto recién creado
cylinder = bpy.context.object
bpy.context.view_layer.objects.active = cylinder

# Ajustar la escala para que tenga el diámetro correcto
cylinder.scale = (2 * radius, 2 * radius, height)

# Guardar el archivo si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene[BLEND_OUT])