import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 10
alto = 1.2

# Crea el muro de contención
bpy.ops.mesh.primitive_cube_add(size=alto, location=(0, 0, alto))
muro = bpy.context.active_object
muro.scale((longitud, alto, 1))

# Crea la baranda metálica
baranda = bpy.data.objects.new("Baranda", bpy.data.meshes.new("Baranda"))
baranda.location = (0, 0, alto + 0.2)
baranda.scale((longitud, 0.5, 0.2))
bpy.context.collection.objects.link(baranda)

# Crea la geometría de los ladrillos
ladrillo = bpy.data.meshes.new("Ladrillo")
verts = []
faces = []

for i in range(int(longitud / 0.1)):
    for j in range(int(alto / 0.1)):
        verts.extend([
            mathutils.Vector((i * 0.1, j * 0.1, 0)),
            mathutils.Vector(((i + 1) * 0.1, j * 0.1, 0)),
            mathutils.Vector(((i + 1) * 0.1, (j + 1) * 0.1, 0)),
            mathutils.Vector((i * 0.1, (j + 1) * 0.1, 0))
        ])
        faces.extend([
            [0, 1, 2],
            [0, 2, 3]
        ])

ladrillo.from_pydata(verts, [], faces)
ladrillo.update(calc_edges=True)

# Crea el objeto de los ladrillos
obj_ladrillo = bpy.data.objects.new("Ladrillos", ladrillo)
bpy.context.collection.objects.link(obj_ladrillo)

# Asigna la materiales y texturas a los objetos
muro.data.materials.append(bpy.data.materials['Material'])
baranda.data.materials.append(bpy.data.materials['Material'])

# Guardar el archivo .blend si se especificó la ruta de salida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])