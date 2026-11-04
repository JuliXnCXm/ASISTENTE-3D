import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura principal con blender_arch ---
muro_fondo = A.crear_muro('Muro_Fondo', largo=5, alto=2.8, grosor=0.3, origen=(-2.5, 0, 0), material='Hormigon')
techo = A.crear_techo_plano('Techo_Vidrio', ancho=5.6, fondo=1.2, espesor=0.05, origen=(-2.8, -0.6, 2.8), material='Vidrio_Templado')

# --- Banco de hormigón con bpy ---
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.45))
banco = bpy.context.active_object
banco.name = 'Banco_Hormigon'
banco.dimensions = (2.0, 0.5, 0.09)
A.asignar_material(banco, nombre='Hormigon', base_color=(0.6, 0.6, 0.6, 1))

# --- Techo de vidrio curvo con bpy ---
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 2.8 + 0.025))
techo_curvo = bpy.context.active_object
techo_curvo.name = 'Techo_Vidrio_Curvo'
techo_curvo.dimensions = (4.8, 1.0, 1)

# Modificador para darle curvatura
mod = techo_curvo.modifiers.new(name='Curva', type='SIMPLE_DEFORM')
mod.deform_method = 'BEND'
mod.angle = 1.5708 # 90 grados en radianes
mod.deform_axis = 'Y'

# Añadir rotación para que el vidrio quede horizontal
bpy.data.objects[techo_curvo.name].rotation_euler[0] = 1.5708

# Material de vidrio con modificador de desplazamiento
A.asignar_material(techo_curvo, nombre='Vidrio_Templado', base_color=(0.9, 0.9, 0.9, 0.8))

# --- Costillas metálicas con bpy ---
for i in range(5):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=2.6, location=(-2.5 + i * 0.8, -0.6, 1.3))
    costilla = bpy.context.active_object
    costilla.name = f'Costilla_{i}'
    A.asignar_material(costilla, nombre='Acero_Inox', base_color=(0.8, 0.8, 0.8, 1))

A.agregar_luz('Luz_Sol', tipo='SUN', ubicacion=(5, -5, 10), energia=3)