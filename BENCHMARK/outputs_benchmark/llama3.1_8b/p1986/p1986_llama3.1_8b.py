import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -1))

# Crea la isla central
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
isla = bpy.context.active_object

# Duplica y gira la isla para crear la forma de la isla
isla_copy = isla.copy()
isla_copy.location = (1.5, 0, 0)
isla_copy.rotation_euler = mathutils.Euler((math.pi/2, 0, 0), 'XYZ')

# Crea los gabinetes
bpy.ops.mesh.primitive_cube_add(size=1, location=(-2, -1, 0))
gabinete1 = bpy.context.active_object

bpy.ops.mesh.primitive_cube_add(size=1, location=(2, -1, 0))
gabinete2 = bpy.context.active_object

# Duplica y gira los gabinetes para crear la forma de los gabinetes
gabinete1_copy = gabinete1.copy()
gabinete1_copy.location = (-3, -1.5, 0)
gabinete1_copy.rotation_euler = mathutils.Euler((math.pi/2, 0, 0), 'XYZ')

gabinete2_copy = gabinete2.copy()
gabinete2_copy.location = (3, -1.5, 0)
gabinete2_copy.rotation_euler = mathutils.Euler((math.pi/2, 0, 0), 'XYZ')

# Crea la encimera de cuarzo
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 1))

# Crea la campana extractora
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 3))
campana = bpy.context.active_object

# Duplica y gira la campana para crear la forma de la campana
campana_copy = campana.copy()
campana_copy.location = (0, 0, 5)
campana_copy.rotation_euler = mathutils.Euler((math.pi/2, 0, 0), 'XYZ')

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])