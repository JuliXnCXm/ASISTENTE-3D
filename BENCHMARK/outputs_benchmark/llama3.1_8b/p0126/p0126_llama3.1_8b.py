import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 4.0
altura = 2.5
espesor = 0.15

# Crea un nuevo objeto para el muro
muro = bpy.data.objects.new("Muro", None)
bpy.context.collection.objects.link(muro)

# Define la geometría del muro como una caja
verts = [
    mathutils.Vector((0, 0, 0)),
    mathutils.Vector((longitud, 0, 0)),
    mathutils.Vector((longitud, altura, 0)),
    mathutils.Vector((0, altura, 0)),
    mathutils.Vector((0, 0, espesor)),
    mathutils.Vector((longitud, 0, espesor)),
    mathutils.Vector((longitud, altura, espesor)),
    mathutils.Vector((0, altura, espesor))
]

edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

faces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7)
]

# Crea la geometría del muro
muro.data = bpy.data.meshes.new("Muro")
muro.data.from_pydata(verts, edges, faces)
muro.data.update()

# Aplica una transformación de escala para que el muro tenga las dimensiones correctas
muro.scale((longitud, altura, espesor))

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])