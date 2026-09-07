import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -1))

# Crea el sofá
sofa = bpy.data.objects.new('Sofa', None)
sofa.empty_display_size = 2.5
sofa.location = (0, 0, 0)

# Agrega los tres asientos del sofá
for i in range(3):
    asiento = bpy.ops.mesh.primitive_cube_add(size=1, location=(i * -1.5, 0, 0))
    bpy.context.collection.objects.link(asiento)
    asiento.name = 'Asiento ' + str(i+1)

# Agrega el respaldo del sofá
respaldo = bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.5))
bpy.context.collection.objects.link(respaldo)
respaldo.name = 'Respaldo'

# Crea la mesa de centro
mesa_centro = bpy.data.objects.new('Mesa Centro', None)
mesa_centro.empty_display_size = 2
mesa_centro.location = (0, -3.5, 1)

# Agrega los cuatro patas de la mesa de centro
for i in range(4):
    pata = bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i * -1.5, 0, 0))
    bpy.context.collection.objects.link(pata)
    pata.name = 'Pata ' + str(i+1)

# Agrega el tapizado del sofá
tapizado = bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
bpy.context.collection.objects.link(tapizado)
tapizado.name = 'Tapizado'

# Aplica la textura de tela gris al tapizado
tapizado.active_material = bpy.data.materials.new('Tela Gris')
tapizado.active_material.diffuse_color = (0.5, 0.5, 0.5)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])