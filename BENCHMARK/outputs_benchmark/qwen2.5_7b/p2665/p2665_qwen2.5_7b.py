import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones
n_steps = 12
step_width = 0.28
overhang_width = 0.18
traverse_width = 1.0

# Crear los peldaños
for i in range(n_steps):
    # Pared frontal
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, -step_width/2 + (i+1)*overhang_width, -i*0.2))
    
    # Pared trasero
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, step_width/2 - (i+1)*overhang_width, -i*0.2))
    
    # Piso
    bpy.ops.mesh.primitive_cube_add(size=traverse_width, location=(0, 0, -i*0.2 - 0.2))

# Ajustar la escena para que todo se vea
bpy.context.scene.camera.location = (3, -1, 2)
bpy.context.view_layer.update()

# Guardar el archivo .blend si existe BLEND_OUT en las variables de entorno
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)