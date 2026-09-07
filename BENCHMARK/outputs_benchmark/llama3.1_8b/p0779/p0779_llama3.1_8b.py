import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades del sofá
sofa_length = 2.5  # metros
sofa_width = 1.0   # metros
sofa_height = 0.8  # metros

# Crea el cuerpo principal del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, sofa_height))
sofa_body = bpy.context.active_object
sofa_body.name = 'Sofa Body'

# Crea la parte trasera del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, 0))
sofa_back = bpy.context.active_object
sofa_back.name = 'Sofa Back'
sofa_back.scale = (1.5, 1.5, 1.5)

# Crea la parte delantera del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, sofa_height))
sofa_front = bpy.context.active_object
sofa_front.name = 'Sofa Front'
sofa_front.scale = (1.5, 1.5, 1.5)

# Crea la parte superior del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, sofa_height + 0.1))
sofa_top = bpy.context.active_object
sofa_top.name = 'Sofa Top'
sofa_top.scale = (1.5, 1.5, 1.5)

# Crea la parte inferior del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, sofa_height - 0.1))
sofa_bottom = bpy.context.active_object
sofa_bottom.name = 'Sofa Bottom'
sofa_bottom.scale = (1.5, 1.5, 1.5)

# Crea la tapicería del sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, sofa_height))
sofa_cushion = bpy.context.active_object
sofa_cushion.name = 'Sofa Cushion'
sofa_cushion.scale = (1.5, 1.5, 1.5)

# Crea la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, -0.4, 0))
table = bpy.context.active_object
table.name = 'Table'

# Aplica materiales al sofá y mesa de centro
sofa_body.data.materials.append(bpy.data.materials['Gray'])
sofa_back.data.materials.append(bpy.data.materials['Gray'])
sofa_front.data.materials.append(bpy.data.materials['Gray'])
sofa_top.data.materials.append(bpy.data.materials['Gray'])
sofa_bottom.data.materials.append(bpy.data.materials['Gray'])
sofa_cushion.data.materials.append(bpy.data.materials['Gray'])
table.data.materials.append(bpy.data.materials['Wood'])

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'] + '.blend')