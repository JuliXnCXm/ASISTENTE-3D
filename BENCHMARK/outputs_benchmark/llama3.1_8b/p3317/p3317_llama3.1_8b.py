import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el pavimento de adoquines de hormigón
pavimento = bpy.data.objects.new('Pavimento', None)
pavimento.empty_display_size = 1.0

# Crea un cuadrado para el pavimento
cuadro_pavimento = bpy.data.meshes.new('Cuadro_Pavimento')
cuadro_pavimento.from_pydata([
    (-5, -5, 0),
    (5, -5, 0),
    (5, 5, 0),
    (-5, 5, 0)
], [], [])
bpy.context.collection.objects.link(pavimento)
pavimento.data = cuadro_pavimento
pavimento.location = mathutils.Vector((0, 0, 0))

# Crea las bancas de diseño simple
banca = bpy.data.objects.new('Banca', None)
banca.empty_display_size = 1.0

# Crea un rectángulo para la banca
rectangulo_banca = bpy.data.meshes.new('Rectangulo_Banca')
rectangulo_banca.from_pydata([
    (-2, -1, 0),
    (2, -1, 0),
    (2, 1, 0),
    (-2, 1, 0)
], [], [])
bpy.context.collection.objects.link(banca)
banca.data = rectangulo_banca
banca.location = mathutils.Vector((0, 5, 0))

# Crea las farolas altas y delgadas para la iluminación nocturna
farola = bpy.data.objects.new('Farola', None)
farola.empty_display_size = 1.0

# Crea un cilindro para la farola
cilindro_farola = bpy.data.meshes.new('Cilindro_Farola')
cilindro_farola.from_pydata([
    (0, -5, 10),
    (0, -5, 15)
], [], [])
bpy.context.collection.objects.link(farola)
farola.data = cilindro_farola
farola.location = mathutils.Vector((0, 0, 20))

# Crea los árboles plantados en alcorques cuadrados
arbol = bpy.data.objects.new('Arbol', None)
arbol.empty_display_size = 1.0

# Crea un cubo para el alcorque
cubo_alcorque = bpy.data.meshes.new('Cubo_Alcorque')
cubo_alcorque.from_pydata([
    (-2, -2, 10),
    (2, -2, 10),
    (2, 2, 10),
    (-2, 2, 10)
], [], [])
bpy.context.collection.objects.link(arbol)
arbol.data = cubo_alcorque
arbol.location = mathutils.Vector((0, 5, 20))

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])