import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear peldaños de hormigón
num_steps = 15
step_height = 0.2  # Altura del peldaño en metros
step_width = 0.4   # Anchura del peldaño en metros
step_depth = 0.1   # Profundidad del peldaño en metros

for i in range(num_steps):
    bpy.ops.mesh.primitive_cube_add(size=step_height, location=(i * step_width, -i * step_height / 2, 0))
    cube = bpy.context.object
    cube.scale.x = step_width / step_height
    cube.scale.y = step_depth / step_height
    cube.name = f"Step_{i}"

# Crear baranda metálica en el descanso superior
barrier_length = 2  # Longitud de la baranda en metros
barrier_width = 0.05  # Anchura de la baranda en metros
barrier_height = 1  # Altura de la baranda en metros

bpy.ops.mesh.primitive_cube_add(size=barrier_width, location=(num_steps * step_width / 2, -(num_steps - 1) * step_height / 2 + barrier_height / 2, 0))
barrier = bpy.context.object
barrier.scale.x = barrier_length / barrier_width
barrier.name = "Barrier"

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])