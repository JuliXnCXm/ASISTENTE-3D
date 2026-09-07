import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear la parcela de tierra
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 0))
terrain = bpy.context.object
terrain.scale.x = 5
terrain.scale.y = 5
terrain.scale.z = 1

# Crear el árbol de copa esférica
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(2.5, 2.5, 3))
tree = bpy.context.object
tree.scale.x = 1
tree.scale.y = 1
tree.scale.z = 4

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])