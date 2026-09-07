import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del terreno
terreno_ancho = 30
terreno_largo = 25

# Define las dimensiones de la casa
casa_ancho = 10
casa_largo = 8

# Define las dimensiones del árbol
arbol_altura = 5
arbol_radio = 1.5

# Crea el terreno
bpy.ops.mesh.primitive_plane_add(size=terreno_ancho, location=(0, -terreno_largo/2, 0))
bpy.context.active_object.name = "Terreno"
bpy.ops.object.modifier_apply(modifier="Subdivision")

# Crea la casa
bpy.ops.mesh.primitive_cube_add(size=casa_ancho, location=(casa_ancho/2, casa_largo/2, 0))
bpy.context.active_object.name = "Casa"
bpy.ops.object.modifier_apply(modifier="Subdivision")
bpy.ops.transform.resize(value=(casa_largo, casa_ancho, casa_ancho))

# Crea el tejado
bpy.ops.mesh.primitive_plane_add(size=casa_ancho, location=(casa_ancho/2, casa_largo/2, casa_ancho))
bpy.context.active_object.name = "Tejado"
bpy.ops.object.modifier_apply(modifier="Subdivision")
bpy.ops.transform.resize(value=(casa_largo, casa_ancho, casa_ancho))

# Crea el árbol
bpy.ops.mesh.primitive_cylinder_add(radius=arbol_radio, depth=arbol_altura, location=(0, 0, arbol_altura))
bpy.context.active_object.name = "Arbol"

# Ubica la casa en el terreno
bpy.context.collection.objects.link(bpy.data.objects['Casa'])
bpy.ops.transform.translate(value=(casa_ancho/2, -terreno_largo/4, 0))

# Ubica el árbol en el terreno
bpy.context.collection.objects.link(bpy.data.objects['Arbol'])
bpy.ops.transform.translate(value=(0, -terreno_largo/2 + arbol_radio, 0))

# Guarda la escena si se especificó un archivo de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene['BLEND_OUT'])