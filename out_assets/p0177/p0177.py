import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro = 0.2
altura_cilindro = 0.9
radio = diametro / 2

# Crear el cuerpo cilíndrico
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio, 
    depth=altura_cilindro, 
    location=(0, 0, altura_cilindro / 2)
)
cilindro = bpy.context.active_object
cilindro.name = "CuerpoBolardo"

# Crear la cabeza semiesférica
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio, 
    location=(0, 0, altura_cilindro)
)
esfera = bpy.context.active_object
esfera.name = "CabezaBolardoTemp"

# Cortar la esfera para hacerla semiesférica
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type='VERT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.translate(value=(0,0,-radio))
bpy.ops.mesh.bisect(plane_co=(0,0,0), plane_no=(0,0,1), clear_inner=True)
bpy.ops.object.mode_set(mode='OBJECT')
esfera.name = "CabezaBolardo"

# Unir las dos partes
bpy.ops.object.select_all(action='DESELECT')
cilindro.select_set(True)
esfera.select_set(True)
bpy.context.view_layer.objects.active = cilindro
bpy.ops.object.join()