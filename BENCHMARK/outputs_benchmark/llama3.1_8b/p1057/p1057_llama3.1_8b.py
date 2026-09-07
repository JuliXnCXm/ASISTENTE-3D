import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades de la escalera
ancho = 1.0  # Ancho en metros
alto_peldaño = 0.2  # Alto del peldaño en metros
profundidad_peldaño = 0.05  # Profundidad del peldaño en metros
num_peldaños = 16

# Crea el objeto de la escalera
escalera = bpy.data.objects.new("Escalera", None)
bpy.context.collection.objects.link(escalera)

# Crea los peldaños
for i in range(num_peldaños):
    # Calcula las coordenadas del peldaño actual
    x = ancho / 2 + (i - num_peldaños // 2) * alto_peldaño
    y = 0

    # Crea el objeto de peldaño
    peldaño = bpy.data.objects.new(f"Peldaño {i+1}", None)
    peldaño.location = mathutils.Vector((x, y, i * profundidad_peldaño))
    bpy.context.collection.objects.link(peldaño)

# Crea la barandilla superior
barandilla_superior = bpy.data.objects.new("Barandilla Superior", None)
bpy.context.collection.objects.link(barandilla_superior)
barandilla_superior.location = mathutils.Vector((ancho / 2, 0, num_peldaños * profundidad_peldaño))
barandilla_superior.scale = (ancho, alto_peldaño, profundidad_peldaño)

# Crea la barandilla inferior
barandilla_inferior = bpy.data.objects.new("Barandilla Inferior", None)
bpy.context.collection.objects.link(barandilla_inferior)
barandilla_inferior.location = mathutils.Vector((ancho / 2, 0, 0))
barandilla_inferior.scale = (ancho, alto_peldaño, profundidad_peldaño)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])