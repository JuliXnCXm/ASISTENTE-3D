import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de los objetos
sofa_length = 2.5  # metros
sofa_width = 1.8   # metros
mesa_centro_length = 0.9  # metros
mesa_centro_width = 0.6  # metros

# Crea el sofá
bpy.ops.mesh.primitive_cube_add(size=sofa_length, location=(0, -sofa_width/2, 0))
obj_software = bpy.context.active_object
obj_software.name = 'Sofa'
obj_software.scale = (sofa_length, sofa_width, 1)

# Crea la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=mesa_centro_length, location=(0, -mesa_centro_width/2, -0.5))
obj_mesa_centro = bpy.context.active_object
obj_mesa_centro.name = 'Mesa Centro'
obj_mesa_centro.scale = (mesa_centro_length, mesa_centro_width, 1)

# Coloca la mesa de centro delante del sofá
bpy.ops.transform.translate(value=(0, -sofa_width/2 + mesa_centro_width/2, -0.5))

# Guardar .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])