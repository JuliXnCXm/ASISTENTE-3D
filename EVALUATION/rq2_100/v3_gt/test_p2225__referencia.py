import blender_arch as A
import bpy
from math import sin, cos, pi

A.limpiar_escena()

# 1. Base de la plaza y luces con blender_arch
A.crear_piso('Plaza', ancho=12, fondo=12, espesor=0.15, origen=(-6,-6,-0.15), material='Porcelanato')

# Luces sumergidas
num_luces = 6
radio_luces = 1.8
for i in range(num_luces):
    angulo = 2 * pi * i / num_luces
    lx = radio_luces * cos(angulo)
    ly = radio_luces * sin(angulo)
    A.agregar_luz(f'Luz_Fuente_{i}', tipo='SPOT', ubicacion=(lx, ly, 0.1), energia=150, color=(0.5, 0.8, 1.0))
    spot_light = bpy.data.objects[f'Luz_Fuente_{i}']
    spot_light.rotation_euler = (0, 0, angulo)

# 2. Vaso de la fuente con bpy
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=3, depth=0.6, location=(0,0,0.3))
vaso_fuente = bpy.context.active_object
vaso_fuente.name = 'Vaso_Fuente'
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
vaso_fuente.data.polygons[-1].select = True # Cara superior
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.inset(thickness=0.2)
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={'value':(0, 0, -0.4)})
bpy.ops.object.mode_set(mode='OBJECT')
A.asignar_material(vaso_fuente, nombre='Hormigon')

# 3. Agua con modificador de ondas bpy
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=2.75, depth=0.01, location=(0,0,0.4))
agua = bpy.context.active_object
agua.name = 'Agua_Fuente'
bpy.ops.object.shade_smooth()
mod_wave = agua.modifiers.new('Ondas', 'WAVE')
mod_wave.height = 0.02
mod_wave.width = 0.8
mod_wave.speed = 0.05
A.asignar_material(agua, nombre='Agua')

# 4. Escultura abstracta con esferas bpy
esferas_locs = [(0, 0, 0.8), (0.2, 0.3, 1.5), (-0.4, 0.1, 2.0), (0.1, -0.5, 2.5)]
esferas_rads = [0.6, 0.4, 0.5, 0.3]
objetos_esfera = []
for i, (loc, rad) in enumerate(zip(esferas_locs, esferas_rads)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, location=loc, segments=32, ring_count=16)
    esfera = bpy.context.active_object
    esfera.name = f'Esfera_{i}'
    bpy.ops.object.shade_smooth()
    objetos_esfera.append(esfera)

# Unir esferas en un solo objeto
bpy.ops.object.select_all(action='DESELECT')
for obj in objetos_esfera:
    obj.select_set(True)
bpy.context.view_layer.objects.active = objetos_esfera[0]
bpy.ops.object.join()
escultura = bpy.context.active_object
escultura.name = 'Escultura_Abstracta'
A.asignar_material(escultura, nombre='Acero_Inox')

A.crear_camara('Camara', ubicacion=(5, -8, 4), rotacion=(75, 0, 30))