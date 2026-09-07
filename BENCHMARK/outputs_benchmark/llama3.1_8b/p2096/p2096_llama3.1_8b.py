import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -0.1))

# Crea la cama con cabecero tapizado
cama = bpy.data.objects.new('Cama', bpy.data.meshes.new('Cama'))
cama.location = (0, 2, 0)
cama.scale = (3, 2, 2)

# Cuerpo de la cama
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, -0.5))
cama_body = bpy.context.active_object
cama_body.name = 'Cuerpo de la cama'
cama_body.parent = cama

# Cabecero de la cama
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, -1.2))
cabecero = bpy.context.active_object
cabecero.name = 'Cabecero de la cama'
cabecero.parent = cama

# Tapizado del cabecero
bpy.ops.mesh.primitive_plane_add(size=1.5, location=(0, 0, -1.2))
tapizado = bpy.context.active_object
tapizado.name = 'Tapizado del cabecero'
tapizado.parent = cabecero

# Muro bajo separador para un vestidor
muro = bpy.data.objects.new('Muro', bpy.data.meshes.new('Muro'))
muro.location = (2, 0, -1.5)
muro.scale = (0.5, 3, 1)

# Armarios empotrados
armario_izquierdo = bpy.data.objects.new('Armario izquierdo', bpy.data.meshes.new('Armario izquierdo'))
armario_izquierdo.location = (-2, -1.5, -1)
armario_izquierdo.scale = (0.5, 3, 1)

armario_derecho = bpy.data.objects.new('Armario derecho', bpy.data.meshes.new('Armario derecho'))
armario_derecho.location = (2, -1.5, -1)
armario_derecho.scale = (0.5, 3, 1)

# Agrega los objetos a la escena
bpy.context.collection.objects.link(cama)
bpy.context.collection.objects.link(muro)
bpy.context.collection.objects.link(armario_izquierdo)
bpy.context.collection.objects.link(armario_derecho)

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene['BLEND_OUT'])