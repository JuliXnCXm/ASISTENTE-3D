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

# Agrega textura al sofá
sofa_body.data.materials.append(bpy.data.materials['GreyFabric'])

# Define las propiedades de la mesa de centro
table_length = 1.5  # metros
table_width = 0.8   # metros
table_height = 0.7  # metros

# Crea el cuerpo de la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=table_length, location=(0, -2.5, table_height))
table_body = bpy.context.active_object
table_body.scale = (table_length, table_width, table_height)

# Agrega material a la mesa de centro
table_body.data.materials.append(bpy.data.materials['WalnutWood'])

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])