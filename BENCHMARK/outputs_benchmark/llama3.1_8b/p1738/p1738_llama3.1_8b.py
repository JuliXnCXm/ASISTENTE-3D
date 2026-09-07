import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades del árbol
radio_copa = 2
alto_copa = 4
alto_tronco = 2.5

# Crea el tronco
tronco = bpy.data.objects.new("Tronco", bpy.data.meshes.new("Tronco"))
tronco.location = mathutils.Vector((0, 0, -alto_tronco))
tronco.scale = (1, 1, alto_tronco)
bpy.context.collection.objects.link(tronco)

# Crea la copa
copa = bpy.data.meshes.new("Copa")
copa.from_pydata([
    (-radio_copa, 0, -alto_copa),
    (radio_copa, 0, -alto_copa),
    (radio_copa, 0, alto_copa),
    (-radio_copa, 0, alto_copa)
], [])
copa.update(calc_edges=True)

bpy.context.collection.objects.link(copa)

# Coloca la copa en su lugar
copa.location = mathutils.Vector((0, 0, -alto_tronco + alto_copa))

# Aplica un material a la copa (opcional)
mat = bpy.data.materials.new("Copa")
mat.diffuse_color = (1, 0.5, 0)
copa.data.materials.append(mat)

if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])