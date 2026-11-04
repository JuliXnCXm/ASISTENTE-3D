import blender_arch as A
import bpy
from math import radians

A.limpiar_escena()

# --- Base y estructura principal con DSL ---
A.crear_piso('Pavimento', ancho=5, fondo=2.5, espesor=0.15, origen=(-2.5, -1.25, -0.15), material='Asfalto')
A.crear_muro('Panel_Trasero', largo=4.0, alto=2.4, grosor=0.05, origen=(-2, 1.0, 0), material='Vidrio')

columnas_origen = [(-2.0, 1.0, 0), (2.0, 1.0, 0)]
for i, origen in enumerate(columnas_origen):
    A.crear_columna(f'Poste_{i}', seccion='circ', diametro=0.1, alto=2.4, origen=origen, material='Acero')

# Banco de hormigón
perfil_banco = [(0,0), (0,0.5), (0.4, 0.5), (0.4, 0.4), (0.1, 0.4), (0.1, 0)]
A.extruir_perfil('Banco', puntos_2d=perfil_banco, altura=3.0, material='Hormigon')
banco = bpy.data.objects['Banco']
banco.location = (-1.5, 0.4, 0)
banco.rotation_euler[0] = radians(90)
banco.rotation_euler[2] = radians(90)

# --- Techo curvado con bpy ---
# Crear la superficie de vidrio
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 2.5))
techo = bpy.context.active_object
techo.name = 'Techo_Vidrio'
techo.dimensions = (4.2, 2.0, 0)
bpy.ops.object.transform_apply(scale=True)
A.asignar_material(techo, nombre='Vidrio_Templado')

# Añadir modificador para curvarlo
mod_solidify = techo.modifiers.new(name='Solidify', type='SOLIDIFY')
mod_solidify.thickness = 0.02
mod_bend = techo.modifiers.new(name='Bend', type='SIMPLE_DEFORM')
mod_bend.deform_method = 'BEND'
mod_bend.angle = radians(-30)
mod_bend.deform_axis = 'X'

# Crear las costillas de soporte
radio_costilla = 0.03
num_costillas = 7
espaciado = 4.0 / (num_costillas - 1)

for i in range(num_costillas):
    x_loc = -2.0 + i * espaciado
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=radio_costilla, location=(x_loc, 0, 1.6), rotation=(radians(90), 0, 0))
    costilla = bpy.context.active_object
    costilla.name = f'Costilla_{i}'
    # Escalar para que sea un arco
    bpy.ops.transform.resize(value=(1, 1.1, 1))
    # Cortar la mitad inferior
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0,0,0), plane_no=(0,0,1), clear_outer=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    A.asignar_material(costilla, nombre='Acero_Inox')