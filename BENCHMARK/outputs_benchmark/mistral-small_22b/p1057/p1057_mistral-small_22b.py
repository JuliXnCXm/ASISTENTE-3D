import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el material del hormigón
material = bpy.data.materials.new(name="Concrete")
material.diffuse_color = (0.5, 0.5, 0.5)

# Crear la escalera
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
escalera = bpy.context.object
escalera.name = "Escalera"

# Aplicar el material al objeto
if material:
    escalera.data.materials.append(material)

# Crear los peldaños
for i in range(16):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, i * 0.2))
    peldaño = bpy.context.object
    peldaño.name = f"Peldaño_{i}"
    if material:
        peldaño.data.materials.append(material)
    escalera.objects.link(peldaño)

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])