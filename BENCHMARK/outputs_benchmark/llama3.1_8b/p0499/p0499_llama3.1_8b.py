import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el plano
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))

# Selecciona el plano
obj = bpy.context.active_object
obj.scale = (15, 1, 1)  # Ajusta la escala del plano

# Crea un nuevo material para el césped
mat = bpy.data.materials.new(name="Cesped")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.3, 1.0, 0.2, 1.0)  # Color del césped

# Aplica el material al plano
obj.data.materials.append(mat)

# Ajusta la altura del plano para que sea un terreno plano
bpy.ops.object.modifier_add(type='ARRAY')
mod = obj.modifiers[-1]
mod.count = 1
mod.use_merge_holes = True

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])