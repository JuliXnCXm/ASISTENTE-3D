import bpy
import mathutils

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establecer las unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crear el perfil para el escritorio L
profile_data = [
    (0, 0.5),  # Punto superior izquierdo
    (1, 0.5),  # Punto superior derecho
    (1.2, 0.8),  # Punto inferior derecho
    (0.2, 0.8)   # Punto inferior izquierdo
]
profile = bpy.data.curves.new('Profile', 'CURVE')
profile.dimensions = '3D'
profile.fill_mode = 'FULL'

# Crear los puntos del perfil
points = []
for x, y in profile_data:
    points.append(mathutils.Vector((x, y, 0)))
profile.points = points

# Crear el objeto de extrusión
extrusion_object = bpy.data.objects.new('Profile', profile)
bpy.context.collection.objects.link(extrusion_object)

# Extruir el perfil para crear el escritorio L
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.extrude_move(curve=bpy.context.active_object, offset=0.1)
bpy.ops.object.mode_set(mode='OBJECT')

# Crear la estantería grande
estanteria = bpy.data.objects.new('Estanteria', None)
estanteria.location = (2, 0, 0)
estanteria.scale = (5, 3, 2)

# Crear la silla
silla = bpy.data.objects.new('Silla', None)
silla.location = (-1.5, -1.5, 0)
silla.scale = (1.5, 1.5, 1.5)

# Agregar objetos a la escena
bpy.context.collection.objects.link(estanteria)
bpy.context.collection.objects.link(silla)

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])