import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del dormitorio principal
ancho = 4.5
profundidad = 3.8
alto_cama = 1.9
alto_muro = 2.0

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=profundidad, location=(0, -ancho/2, 0))
bpy.context.active_object.name = "Suelo"
bpy.ops.object.modifier_apply(modifier="Subdivision")

# Crea la cama con cabecero tapizado
bpy.ops.mesh.primitive_cube_add(size=alto_cama, location=(0, -ancho/2 + 1.5, profundidad/2))
cama = bpy.context.active_object
cama.name = "Cama"
bpy.ops.object.modifier_apply(modifier="Subdivision")
# Crea el cabecero de la cama
bpy.ops.mesh.primitive_cube_add(size=alto_cama + 0.5, location=(0, -ancho/2 + 1.5, profundidad/2))
cabecero = bpy.context.active_object
cabecero.name = "Cabecero"
bpy.ops.object.modifier_apply(modifier="Subdivision")
# Ajusta la forma del cabecero para que sea un rectángulo
cabecero.data.shape_keys.keynames.remove("Basis")
cabecero.data.shape_keys.keynames.insert(1, "Width")
cabecero.data.shape_keys.keynames.insert(2, "Height")
cabecero.data.shape_keys.value_path_edit = "Width"
cabecero.data.shape_keys.keyframes_insert_set(0)
cabecero.data.shape_keys.keyframes_insert_set(1)

# Crea el muro bajo separador para un vestidor
bpy.ops.mesh.primitive_cube_add(size=alto_muro, location=(0, -ancho/2 + 1.5, profundidad/2))
muro = bpy.context.active_object
muro.name = "Muro"
bpy.ops.object.modifier_apply(modifier="Subdivision")

# Crea los armarios empotrados
bpy.ops.mesh.primitive_cube_add(size=alto_muro, location=(0, -ancho/2 + 1.5, profundidad/2))
armario_izquierdo = bpy.context.active_object
armario_izquierdo.name = "Armario Izquierdo"
bpy.ops.object.modifier_apply(modifier="Subdivision")
bpy.ops.mesh.primitive_cube_add(size=alto_muro, location=(0, -ancho/2 + 1.5, profundidad/2))
armario_derecho = bpy.context.active_object
armario_derecho.name = "Armario Derecho"
bpy.ops.object.modifier_apply(modifier="Subdivision")

# Guarda el archivo .blend si se especificó la ruta en la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])