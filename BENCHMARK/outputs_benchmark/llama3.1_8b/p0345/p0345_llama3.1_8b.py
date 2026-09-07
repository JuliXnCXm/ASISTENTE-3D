import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades de la escalera
escalera = {
    'alto': 2,  # Alto de cada peldaño en metros
    'ancho': 0.5,  # Ancho de cada peldaño en metros
    'profundidad': 0.1,  # Profundidad del descanso superior en metros
    'longitud_baranda': 10,  # Longitud de la baranda lineal metálica en metros
}

# Crea el cuerpo de la escalera
bpy.ops.mesh.primitive_cube_add(size=escalera['alto'], location=(0, 0, -15))
escalera_cuerpo = bpy.context.active_object

# Duplica y alinea los peldaños
for i in range(1, 16):
    bpy.ops.object.duplicate_move_linked()
    bpy.context.active_object.location = (i * escalera['ancho'], 0, -15 + (i - 1) * escalera['alto'])
    bpy.ops.object.modifier_add(type='ARRAY')
    bpy.context.active_object.modifiers[-1].name = 'Array'
    bpy.context.active_object.modifiers['Array'].offset = i
    bpy.context.active_object.modifiers['Array'].cycles_visibility = False

# Crea el descanso superior
bpy.ops.mesh.primitive_cube_add(size=escalera['alto'], location=(0, 0, -15))
descanso_superior = bpy.context.active_object
descanso_superior.scale = (escalera['ancho'], escalera['profundidad'], escalera['alto'])

# Crea la baranda lineal metálica
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -15 + escalera['alto']))
baranda = bpy.context.active_object
baranda.scale = (escalera['ancho'], 0.05, escalera['longitud_baranda'])

# Alinea la baranda con el descanso superior
bpy.ops.object.select_all(action='DESELECT')
descanso_superior.select_set(True)
baranda.select_set(True)
bpy.context.view_layer.objects.active = descanso_superior
bpy.ops.object.join()

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])