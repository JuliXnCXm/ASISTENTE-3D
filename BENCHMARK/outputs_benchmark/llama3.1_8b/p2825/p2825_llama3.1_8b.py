import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del bolardo
diameter = 0.2
height = 0.9

# Crea un cilindro en el origen
bpy.ops.mesh.primitive_cylinder_add(radius=diameter/2, depth=height, enter_editmode=False, location=(0, 0, 0))

# Aplica una materiales de hormigón
mat = bpy.data.materials.new(name="Concrete")
mat.diffuse_color = (0.8, 0.6, 0.4)
bpy.context.object.data.materials.append(mat)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])