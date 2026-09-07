import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear la parcela de tierra
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -2.5))
terrain = bpy.context.object
terrain.scale = (5, 5, 5)

# Crear el árbol de copa esférica
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 2))
tree = bpy.context.object

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])