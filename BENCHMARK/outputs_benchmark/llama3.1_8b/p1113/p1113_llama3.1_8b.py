import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
bpy.context.object.name = "Suelo"
bpy.context.object.scale = (4, 3.5, 0.1)

# Crea la pared del fondo
bpy.ops.mesh.primitive_cube_add(size=3.5, location=(-2, 0, 0))
bpy.context.object.name = "Pared Fondo"
bpy.context.object.scale = (3.5, 4, 2)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi/2, 0, 0))

# Crea la pared del lado izquierdo
bpy.ops.mesh.primitive_cube_add(size=4, location=(-2, -1.75, 0))
bpy.context.object.name = "Pared Izquierda"
bpy.context.object.scale = (4, 3.5, 2)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi/2, 0, 0))

# Crea la pared del lado derecho
bpy.ops.mesh.primitive_cube_add(size=4, location=(1.75, -1.75, 0))
bpy.context.object.name = "Pared Derecha"
bpy.context.object.scale = (4, 3.5, 2)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi/2, 0, 0))

# Crea la pared del techo
bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, 2))
bpy.context.object.name = "Pared Techo"
bpy.context.object.scale = (4, 3.5, 2)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi/2, 0, 0))

# Pinta las paredes de gris
bpy.data.materials.new(name="Gris")
mat = bpy.data.materials["Gris"]
mat.diffuse_color = (0.5, 0.5, 0.5)
for obj in bpy.context.scene.objects:
    if "Pared" in obj.name and obj.type == 'MESH':
        obj.data.materials.append(mat)

# Crea la cama doble
bpy.ops.mesh.primitive_cube_add(size=2, location=(-1.75, -0.875, 0))
bpy.context.object.name = "Cama Doble"
bpy.context.object.scale = (2, 2, 1)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi/2, 0, 0))

# Crea la estructura de madera
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-1.75, -0.875, 0))
bpy.context.object.name = "Estructura Madera"
bpy.context.object.scale = (2, 0.5, 0.5)
bpy.context.object.rotation_euler = mathutils.Vector((math.pi/2, 0, 0))

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])