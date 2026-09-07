import bpy
import mathutils
import bmesh

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))

# Crea la alfombra
bpy.ops.mesh.primitive_cube_add(size=5, location=(0, -2.5, 0))
bpy.context.active_object.name = 'Alfombra'
bpy.data.materials.new('Alfombra')
mat = bpy.data.materials['Alfombra']
mat.diffuse_color = (1, 1, 1)
bpy.ops.object.material_slot_add()
bpy.context.active_object.active_material = mat

# Crea el sofá
sofa = bpy.data.objects.new('Sofa', None)
bpy.context.collection.objects.link(sofa)

# Crea la geometría del sofá
verts = [
    mathutils.Vector((0, 0, 0)),
    mathutils.Vector((-2.5, -1.25, 0)),
    mathutils.Vector((-2.5, 1.25, 0)),
    mathutils.Vector((2.5, 1.25, 0)),
    mathutils.Vector((2.5, -1.25, 0)),
    mathutils.Vector((0, 0, 0))
]
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5)
]

bmesh.from_mesh(bpy.context.active_object.data).verts.extend(verts)
bmesh.from_mesh(bpy.context.active_object.data).edges.extend(edges)

# Crea la estantería
estanteria = bpy.data.objects.new('Estanteria', None)
bpy.context.collection.objects.link(estanteria)

# Crea la geometría de la estantería
verts = [
    mathutils.Vector((0, 2.5, 1)),
    mathutils.Vector((-1.25, -1.25, 1)),
    mathutils.Vector((1.25, -1.25, 1)),
    mathutils.Vector((1.25, 1.25, 1)),
    mathutils.Vector((-1.25, 1.25, 1))
]
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 0)
]

bmesh.from_mesh(bpy.context.active_object.data).verts.extend(verts)
bmesh.from_mesh(bpy.context.active_object.data).edges.extend(edges)

# Aplica un modificador de curvatura para dar forma a la estantería
mod = bpy.ops.object.modifier_apply(modifier='CURVE')

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.context.scene.render.filepath = os.environ['BLEND_OUT']
    bpy.ops.wm.save_mainfile()