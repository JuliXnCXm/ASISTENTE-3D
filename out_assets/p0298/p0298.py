import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Parámetros
diametros = [3.0, 1.5, 0.7]
alturas_pedestal = [0, 0.8, 0.6]
alturas_cuenco = [0.4, 0.25, 0.15]
espesor_cuenco = 0.1
radio_pedestal = 0.2

def crear_cuenco(diametro, altura, espesor, z_base):
    # Crea una esfera UV, la corta por la mitad y la solidifica
    radio = diametro / 2
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radio,
        segments=64,
        ring_count=32,
        location=(0, 0, z_base + altura)
    )
    sphere = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, z_base + altura), plane_no=(0, 0, 1), clear_outer=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    solidify = sphere.modifiers.new('Solidify', 'SOLIDIFY')
    solidify.thickness = espesor
    bpy.ops.object.modifier_apply(modifier=solidify.name)
    return sphere

def crear_pedestal(radio, altura, z_base):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radio,
        depth=altura,
        location=(0, 0, z_base + altura / 2)
    )
    return bpy.context.active_object

# Crear los niveles
z_actual = 0
objetos_fuente = []

for i in range(len(diametros)):
    # Crear pedestal (excepto para la base)
    if i > 0:
        pedestal = crear_pedestal(radio_pedestal / (i*0.75+1), alturas_pedestal[i], z_actual)
        pedestal.name = f'Pedestal_{i}'
        objetos_fuente.append(pedestal)
        z_actual += alturas_pedestal[i]

    # Crear cuenco
    cuenco = crear_cuenco(diametros[i], alturas_cuenco[i], espesor_cuenco, z_actual)
    cuenco.name = f'Cuenco_{i}'
    objetos_fuente.append(cuenco)
    z_actual += alturas_cuenco[i]

# Unir todas las partes
for obj in bpy.context.scene.objects:
    obj.select_set(False)
for obj in objetos_fuente:
    obj.select_set(True)

if objetos_fuente:
    bpy.context.view_layer.objects.active = objetos_fuente[0]
    bpy.ops.object.join()
    bpy.context.active_object.name = 'FuenteOrnamental'