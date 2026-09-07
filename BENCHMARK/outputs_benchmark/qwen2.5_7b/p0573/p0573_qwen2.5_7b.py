import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el terreno plano de césped
terreno = bpy.data.meshes.new(name="Césped")
obj = bpy.data.objects.new("Terreno", terreno)
bpy.context.collection.objects.link(obj)

# Definir la geometría del terreno
verts = [(x, y, 0) for x in range(-10, 11) for y in range(-7.5, 7.6)]
faces = []

for i in range(20):
    for j in range(14):
        faces.append((i * 15 + j, i * 15 + j + 1, (i + 1) * 15 + j + 1, (i + 1) * 15 + j))

terreno.from_pydata(verts, [], faces)
terreno.update()

# Ajustar la escala para que sea de 20x15 metros
bpy.context.view_layer.objects.active = obj
obj.scale = (20, 15, 1)

if "BLEND_OUT" in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene["BLEND_OUT"])