import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 10  # metros
altura = 1.2   # metros

# Crea el muro de contención
bpy.ops.mesh.primitive_cube_add(size=altura, location=(0, 0, altura))
muro = bpy.context.active_object
muro.scale((longitud, longitud, 1))

# Crea la baranda metálica
baranda = bpy.data.objects.new("Baranda", bpy.data.meshes.new("Baranda"))
baranda.location = (0, 0, altura + 0.5)
baranda.scale((10, 0.2, 0.2))
bpy.context.collection.objects.link(baranda)

# Crea la geometría de los ladrillos
ladrillo = bpy.data.meshes.new("Ladrillo")
ladrillo.from_pydata([
    (-0.5, -0.5, 0),
    (0.5, -0.5, 0),
    (0.5, 0.5, 0),
    (-0.5, 0.5, 0),
    (-0.5, -0.5, 0)
], [], [])
ladrillo.update(calc_edges=True)

# Crea la geometría del muro
muro_mesh = bpy.data.meshes.new("Muro")
muro_mesh.from_pydata([
    (0, 0, altura),
    (longitud, 0, altura),
    (longitud, longitud, altura),
    (0, longitud, altura),
    (0, 0, altura)
], [], [])
muro_mesh.update(calc_edges=True)

# Asigna la geometría del ladrillo al muro
muro.data = ladrillo

# Aplica una textura de ladrillos al muro
bpy.ops.object.modifier_add(type='TEXTURE')
modificador = bpy.context.active_object.modifiers[-1]
modificador.texture_coords = 'UV'
modificador.uv_layer_name = "Ladrillos"

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])