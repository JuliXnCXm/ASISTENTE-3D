import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA PRINCIPAL CON DSL ---
A.crear_losa_rectangular('Losa_Principal', ancho=12, fondo=10, espesor=0.2, origen=(0,0,-0.1), material='Concreto_Piso')
A.crear_muro('Muro_Fondo', largo=12, alto=6, grosor=0.3, origen=(-6,5,0), material='Hormigon')
A.crear_muro('Muro_Frente', largo=12, alto=6, grosor=0.3, origen=(-6,-5,0), material='Hormigon')
A.crear_columna('Columna_Izq', seccion='rect', ancho=0.4, fondo=0.4, alto=6, origen=(-6,0,0), material='Hormigon')
A.crear_columna('Columna_Der', seccion='rect', ancho=0.4, fondo=0.4, alto=6, origen=(6,0,0), material='Hormigon')

# --- MEZZANINE CON MALLA METÁLICA EN BPY ---
# Crear la base del mezzanine
bpy.ops.mesh.primitive_cube_add(location=(0,0,3.5))
mezzanine_base = bpy.context.active_object
mezzanine_base.name = 'Mezzanine_Base'
mezzanine_base.dimensions = (10, 8, 0.2)
A.asignar_material(mezzanine_base, nombre='Acero_Inox', base_color=(0.7, 0.7, 0.7, 1))

# Modificador Wireframe para crear la malla
mod_wire = mezzanine_base.modifiers.new(name='Wireframe', type='WIREFRAME')
mod_wire.thickness = 0.02
mod_wire.width = 1.0
mod_wire.use_even_offset = True
mod_wire.use_relative = False

# Modificador Solidify para dar grosor a la malla
mod_solidify = mezzanine_base.modifiers.new(name='Solidify', type='SOLIDIFY')
mod_solidify.thickness = 0.02

# Barandas con bpy
# Baranda delantera
bpy.ops.mesh.primitive_cube_add(location=(0, -5, 3.5 + 0.02))
baranda_frontal = bpy.context.active_object
baranda_frontal.name = 'Baranda_Frontal'
baranda_frontal.dimensions = (10, 0.1, 0.02)
A.asignar_material(baranda_frontal, nombre='Acero_Inox', base_color=(0.7, 0.7, 0.7, 1))

# Baranda trasera
bpy.ops.mesh.primitive_cube_add(location=(0, 5, 3.5 + 0.02))
baranda_trasera = bpy.context.active_object
baranda_trasera.name = 'Baranda_Trasera'
baranda_trasera.dimensions = (10, 0.1, 0.02)
A.asignar_material(baranda_trasera, nombre='Acero_Inox', base_color=(0.7, 0.7, 0.7, 1))

# Postes
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=7, location=(0, 0, 3.5 + 0.02))
poste_izq = bpy.context.active_object
poste_izq.name = 'Poste_Izq'
A.asignar_material(poste_izq, nombre='Acero_Inox', base_color=(0.7, 0.7, 0.7, 1))
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=7, location=(10, 0, 3.5 + 0.02))
poste_der = bpy.context.active_object
poste_der.name = 'Poste_Der'
A.asignar_material(poste_der, nombre='Acero_Inox', base_color=(0.7, 0.7, 0.7, 1))