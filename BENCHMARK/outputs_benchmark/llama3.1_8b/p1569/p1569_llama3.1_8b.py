import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea un objeto para el edificio
edificio = bpy.data.objects.new('Edificio', None)
bpy.context.collection.objects.link(edificio)

# Define las propiedades del edificio
edificio.location = mathutils.Vector((0, 0, 0))
edificio.scale = (15, 12, 4)  # Ancho, profundidad y altura

# Crea la estructura de columnas
columna = bpy.data.objects.new('Columna', None)
bpy.context.collection.objects.link(columna)

columna.location = mathutils.Vector((0, 0, 0))
columna.scale = (1, 1, 4)  # Ancho, profundidad y altura

# Crea las columnas en cada esquina del edificio
for i in range(4):
    columna_copy = columna.copy()
    bpy.context.collection.objects.link(columna_copy)
    
    if i == 0:  # Esquina superior izquierda
        columna_copy.location = mathutils.Vector((-7.5, -6, 3))
    elif i == 1:  # Esquina superior derecha
        columna_copy.location = mathutils.Vector((7.5, -6, 3))
    elif i == 2:  # Esquina inferior izquierda
        columna_copy.location = mathutils.Vector((-7.5, -6, -3))
    else:  # Esquina inferior derecha
        columna_copy.location = mathutils.Vector((7.5, -6, -3))

# Crea las ventanas en cada fachada
ventana = bpy.data.objects.new('Ventana', None)
bpy.context.collection.objects.link(ventana)

ventana.location = mathutils.Vector((-7.5, 0, 2))
ventana.scale = (1, 2, 2)  # Ancho, profundidad y altura

# Crea las ventanas en cada fachada
for i in range(4):
    ventana_copy = ventana.copy()
    bpy.context.collection.objects.link(ventana_copy)
    
    if i == 0:  # Fachada frontal
        ventana_copy.location = mathutils.Vector((-7.5, 0, 2))
    elif i == 1:  # Fachada trasera
        ventana_copy.location = mathutils.Vector((7.5, 0, -2))
    elif i == 2:  # Fachada izquierda
        ventana_copy.location = mathutils.Vector((-7.5, 6, 2))
    else:  # Fachada derecha
        ventana_copy.location = mathutils.Vector((7.5, 6, -2))

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])