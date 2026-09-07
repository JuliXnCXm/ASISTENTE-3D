import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.5))
bpy.context.object.scale = (10, 10, 1)

# Crear la cama con cabecero tapizado
bpy.ops.mesh.primitive_cube_add(size=2, location=(-3, 0, 0.8))
bpy.ops.transform.resize(value=(2, 2, 0.5))

# Tapicería del cabecero
cabecero = bpy.data.objects.new(name="Cabecero", object_data=bpy.data.meshes.new("CabeceroMesh"))
bpy.context.collection.objects.link(cabecero)
bpy.ops.mesh.primitive_cube_add(size=2, location=(-3, 0, 1.5))
bpy.ops.transform.resize(value=(2, 2, 0.5))
cabecero.data = bpy.context.object.data

# Crear el muro bajo separador
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, -4, 0))
bpy.context.object.scale = (6, 1, 3)

# Crear los armarios empotrados
for i in range(2):
    bpy.ops.mesh.primitive_cube_add(size=1.5, location=(-4 + 3 * i, -4, 1.5))
    bpy.ops.transform.resize(value=(1.5, 1.5, 2))

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if "BLEND_OUT" in os.environ:
    blend_out = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)