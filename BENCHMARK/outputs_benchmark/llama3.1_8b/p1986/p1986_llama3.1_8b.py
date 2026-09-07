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
isle = bpy.data.objects['Plane']
isle.name = 'Isla'
isle.location = (0, 2, 0)
isle.scale = (3, 2, 1)

# Crea los gabinetes
cabinet = bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5, 1.5, 1))
cabinet.name = 'Gabinete'
cabinet.location = (-1.5, 0, 1)
cabinet.scale = (2, 1, 1)

# Crea la encimera de cuarzo
countertop = bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 1.5, 1))
countertop.name = 'Encimera'
countertop.location = (0, 0, 1)
countertop.scale = (3, 2, 0.1)

# Crea la campana extractora
extractor = bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=(0, 0, 2))
extractor.name = 'Campana'
extractor.location = (0, 0, 3)
extractor.scale = (1, 1, 1)

# Ajusta la escala de los objetos
isle.scale = (3, 2, 1)
cabinet.scale = (2, 1, 1)
countertop.scale = (3, 2, 0.1)
extractor.scale = (1, 1, 1)

# Guarda el archivo .blend si se especificó la ruta
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])