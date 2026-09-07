import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -1))

# Crea la pared del fondo
bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, -2))
bpy.context.active_object.name = 'Pared del Fondo'

# Crea la pared lateral izquierda
bpy.ops.mesh.primitive_cube_add(size=4, location=(-2.5, 0, -1))
bpy.context.active_object.name = 'Pared Lateral Izquierda'

# Crea la pared lateral derecha
bpy.ops.mesh.primitive_cube_add(size=4, location=(2.5, 0, -1))
bpy.context.active_object.name = 'Pared Lateral Derecha'

# Crea el techo
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 1))

# Crea el sofá
sofa = bpy.data.objects.new('Sofa', bpy.data.meshes.new('Sofa'))
sofa.location = (0, -2.5, -1)
sofa.scale = (3, 2, 1)

verts = [
    mathutils.Vector((0, -1, 0)),
    mathutils.Vector((2, -1, 0)),
    mathutils.Vector((2, 1, 0)),
    mathutils.Vector((0, 1, 0)),
    mathutils.Vector((-1, 0, 0)),
    mathutils.Vector((1, 0, 0))
]

faces = [
    (0, 1, 2, 3),
    (4, 5, 2, 1)
]

edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 2),
    (2, 1)
]

sofa.data.from_pydata(verts, edges, faces)
bpy.context.collection.objects.link(sofa)

# Crea la mesa de centro
mesa = bpy.data.objects.new('Mesa', bpy.data.meshes.new('Mesa'))
mesa.location = (0, -3.5, 0)
mesa.scale = (2, 1, 0.5)

verts = [
    mathutils.Vector((0, -0.25, 0)),
    mathutils.Vector((-1, -0.25, 0)),
    mathutils.Vector((-1, 0.25, 0)),
    mathutils.Vector((0, 0.25, 0))
]

faces = [
    (0, 1, 2, 3)
]

edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
]

mesa.data.from_pydata(verts, edges, faces)
bpy.context.collection.objects.link(mesa)

# Aplica el material al sofá
sofa_mat = bpy.data.materials.new('Sofa_Material')
sofa_mat.diffuse_color = (0.5, 0.5, 0.5, 1)
sofa_mat.specular_intensity = 0.2

sofa.data.materials.append(sofa_mat)

# Aplica el material a la mesa
mesa_mat = bpy.data.materials.new('Mesa_Material')
mesa_mat.diffuse_color = (0.8, 0.6, 0.4, 1)
mesa_mat.specular_intensity = 0.2

mesa.data.materials.append(mesa_mat)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])