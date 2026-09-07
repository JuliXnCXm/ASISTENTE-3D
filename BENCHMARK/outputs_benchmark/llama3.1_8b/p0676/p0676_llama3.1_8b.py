import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades del sofá
sofa_length = 3.5  # metros
sofa_width = 1.8   # metros
sofa_height = 0.9  # metros

# Crea el cuerpo del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -2, 0))
sofa_body = bpy.context.active_object
sofa_body.scale = (sofa_length, sofa_width, sofa_height)

# Agrega la textura de tela gris al sofá
sofa_body.data.materials.append(bpy.data.materials['Material.001'])

# Define las propiedades de la mesa de centro
mesa_length = 1.2  # metros
mesa_width = 0.8   # metros
mesa_height = 0.5  # metros

# Crea el cuerpo de la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=mesa_length, location=(0, -3, 0))
mesa_body = bpy.context.active_object
mesa_body.scale = (mesa_length, mesa_width, mesa_height)

# Agrega la textura de madera al cuerpo de la mesa de centro
mesa_body.data.materials.append(bpy.data.materials['Material.002'])

# Guarda el archivo .blend si se especificó una ruta de salida en la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])