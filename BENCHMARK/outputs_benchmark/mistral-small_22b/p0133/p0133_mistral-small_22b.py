import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Parámetros de la escalera
ancho = 1.0
huella = 0.3
contrahuella = 0.18
num_peldaños = 15

# Crear los peldaños
for i in range(num_peldaños):
    bpy.ops.mesh.primitive_cube_add(size=huella, location=(i * (huella + contrahuella), huella / 2, ancho / 2))
    bpy.context.object.name = f"Peldaño_{i}"

# Crear la estructura de la escalera
bpy.ops.mesh.primitive_cube_add(size=1, location=(num_peldaños * (huella + contrahuella) / 2, huella / 2, ancho / 2))
bpy.context.object.name = "Estructura"

# Crear los barandales (opcional)
for i in range(num_peldaños):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=huella + contrahuella, location=(i * (huella + contrahuella), huella / 2, ancho))
    bpy.context.object.name = f"Barandal_{i}"

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])