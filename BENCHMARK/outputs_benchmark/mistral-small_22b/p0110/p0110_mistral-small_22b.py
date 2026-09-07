import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Parámetros de la escalera
ancho = 1.0
huella = 0.3
contrahuella = 0.18
num_peldaños = 15
altura_total = huella * num_peldaños + contrahuella * (num_peldaños - 1)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, altura_total / 2))

# Función para crear un peldaño
def create_peldaño(location):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.scale = (ancho / 2, huella / 2, contrahuella / 2)

# Crear los peldaños
for i in range(num_peldaños):
    create_peldaño((0, i * (huella + contrahuella), altura_total / 2 - i * (huella + contrahuella)))

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])