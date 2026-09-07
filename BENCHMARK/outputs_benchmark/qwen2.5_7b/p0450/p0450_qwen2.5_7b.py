import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el cuerpo de la cama (estructura de madera)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.5))
bpy.ops.transform.resize(value=(2, 1, 0.1))

# Crear el colchón (cuboido blanco)
colchon = bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.1, location=(0, 0, -0.5))
bpy.context.object.name = "Colchon"
bpy.data.objects["Colchon"].data.materials.append(bpy.data.materials.new(name="Blanco"))
bpy.data.materials["Blanco"].diffuse_color = (1, 1, 1, 1)

# Ajustar la escena
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.scale = (0.01, 0.01, 0.01)  # Convertir a metros

# Guardar el archivo blend si existe BLEND_OUT
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])