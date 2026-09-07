import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=10)
bpy.context.object.name = "Suelo"
bpy.context.object.location = mathutils.Vector((0, 0, 0))

# Crea la pared del fondo
bpy.ops.mesh.primitive_cube_add(size=5)
bpy.context.object.name = "Pared Fondo"
bpy.context.object.location = mathutils.Vector((0, 0, -2.5))
bpy.context.object.rotation_euler = (math.radians(90), 0, 0)

# Crea la pared del lado izquierdo
bpy.ops.mesh.primitive_cube_add(size=5)
bpy.context.object.name = "Pared Izquierda"
bpy.context.object.location = mathutils.Vector((-2.5, 0, -1))
bpy.context.object.rotation_euler = (math.radians(90), 0, 0)

# Crea la pared del lado derecho
bpy.ops.mesh.primitive_cube_add(size=5)
bpy.context.object.name = "Pared Derecha"
bpy.context.object.location = mathutils.Vector((2.5, 0, -1))
bpy.context.object.rotation_euler = (math.radians(90), 0, 0)

# Crea la pared del techo
bpy.ops.mesh.primitive_cube_add(size=5)
bpy.context.object.name = "Pared Techo"
bpy.context.object.location = mathutils.Vector((0, 0, -3))
bpy.context.object.rotation_euler = (math.radians(90), 0, 0)

# Crea el sofá
bpy.ops.mesh.primitive_cube_add(size=2)
bpy.context.object.name = "Sofa"
bpy.context.object.location = mathutils.Vector((-1.5, -1.5, -1))
bpy.context.object.scale = (3, 2, 0.5)

# Crea la tapicería del sofá
bpy.ops.mesh.primitive_plane_add(size=2)
bpy.context.object.name = "Tapiceria"
bpy.context.object.location = mathutils.Vector((-1.5, -1.5, -1))
bpy.context.object.rotation_euler = (math.radians(90), 0, 0)
bpy.ops.mesh.primitive_cube_add(size=2)
bpy.context.object.name = "Tapiceria"
bpy.context.object.location = mathutils.Vector((-1.5, -1.5, -1))
bpy.context.object.scale = (3, 2, 0.5)

# Crea la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.context.object.name = "Mesa Centro"
bpy.context.object.location = mathutils.Vector((0, 0, -2))

# Aplica textura al sofá y a la tapicería
sofa_mat = bpy.data.materials.new(name="SofaMat")
sofa_mat.diffuse_color = (0.5, 0.5, 0.5)
bpy.context.object.data.materials.append(sofa_mat)

tapiceria_mat = bpy.data.materials.new(name="TapiceriaMat")
tapiceria_mat.diffuse_color = (0.5, 0.5, 0.5)
bpy.context.object.data.materials.append(tapiceria_mat)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])