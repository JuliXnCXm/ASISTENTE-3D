import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la acera
acera_largo = 10
acera_ancho = 2
acera_alto = 0.15

# Dimensiones de la calzada
calzada_ancho = 6
calzada_alto = 0.2

# Dimensiones de la baranda
baranda_alto = 0.9
baranda_grosor = 0.1
baranda_largo = acera_largo

# Crear la acera
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
acera = bpy.context.object
acera.name = "Acera"
acera.scale = (acera_largo/2, acera_ancho/2, acera_alto/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Crear la calzada
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, -acera_ancho - calzada_ancho/2, 0))
calzada = bpy.context.object
calzada.name = "Calzada"
calzada.scale = (acera_largo/2, calzada_ancho/2, calzada_alto/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Crear la baranda
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
baranda = bpy.context.object
baranda.name = "Baranda"
baranda.scale = (baranda_largo/2, baranda_grosor/2, baranda_alto/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Duplicar la baranda a lo largo de la acera
for i in range(1, int(acera_largo)):
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
    baranda_duplicado = bpy.context.object
    baranda_duplicado.location.x += i
    baranda_duplicado.name = "Baranda"

# Unir las barandas en un solo objeto
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.name.startswith("Baranda"):
        obj.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[0]
bpy.ops.object.join()
baranda_unido = bpy.context.object
baranda_unido.name = "Baranda_Unido"

# Mover la baranda a la parte superior de la acera
baranda_unido.location.z += acera_alto

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
try:
    blend_out = bpy.context.preferences.filepaths.file_paths[0]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)
except:
    pass