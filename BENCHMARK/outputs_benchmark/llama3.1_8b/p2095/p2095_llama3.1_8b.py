import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -1))

# Crea la alfombra
bpy.ops.mesh.primitive_cube_add(size=5, location=(0, 0, -2))
bpy.context.active_object.name = 'Alfombra'
bpy.context.object.data.materials.append(bpy.data.materials['Material.001'])

# Crea el sofá modular
sofa = bpy.data.objects.new('Sofa', bpy.data.meshes.new('Sofa'))
sofa.location = (0, 0, -3)
sofa.scale = (2, 1, 1)

verts = [
    (-1.5, -1.5, 0),
    (1.5, -1.5, 0),
    (1.5, 1.5, 0),
    (-1.5, 1.5, 0),
    (-2.5, 0, 0),
    (2.5, 0, 0)
]

edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (0, 4),
    (1, 5),
    (2, 4),
    (3, 5)
]

faces = [
    (0, 1, 2, 3),
    (4, 5, 0, 1),
    (0, 1, 5, 4),
    (1, 2, 4, 5),
    (2, 3, 5, 4),
    (3, 0, 4, 5)
]

sofa.data.from_pydata(verts, edges, faces)
bpy.context.collection.objects.link(sofa)

# Crea la estantería
estanteria = bpy.data.objects.new('Estanteria', bpy.data.meshes.new('Estanteria'))
estanteria.location = (3, 0, -4)
estanteria.scale = (2, 1.5, 1)

verts = [
    (-1.5, -1.5, 0),
    (1.5, -1.5, 0),
    (1.5, 1.5, 0),
    (-1.5, 1.5, 0)
]

edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
]

faces = [
    (0, 1, 2, 3)
]

estanteria.data.from_pydata(verts, edges, faces)
bpy.context.collection.objects.link(estanteria)

# Aplica modificadores a la estantería
modificador_curva = bpy.data.objects.new('Curva', None)
modificador_curva.type = 'CURVE'
modificador_curva.data = bpy.data.curves.new('Estanteria_Curva', type='NURBS_CURVE')
estanteria.modifiers.link(modificador_curva)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])