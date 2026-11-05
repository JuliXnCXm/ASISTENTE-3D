import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA PRINCIPAL CON DSL ---
A.crear_piso('Losa', ancho=10, fondo=8, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')
A.crear_muro('Muro_Fondo', largo=10, alto=6, grosor=0.3, origen=(-5,4,0), material='Hormigon')
A.crear_muro('Muro_Frente', largo=10, alto=6, grosor=0.3, origen=(5,4,0), material='Hormigon')
A.crear_columna('Columna_1', seccion='rect', ancho=0.4, fondo=0.4, alto=6, origen=(-3, -3, 0), material='Hormigon')
A.crear_columna('Columna_2', seccion='rect', ancho=0.4, fondo=0.4, alto=6, origen=(3, -3, 0), material='Hormigon')

# --- MEZZANINE CON MALLA METÁLICA EN BPY ---
# Crear la base del mezzanine
A.crear_piso('Mezzanine', ancho=6, fondo=4, espesor=0.2, origen=(0,0,3.2), material='Acero_Inox')

# Crear la malla para la baranda
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,3.4))
baranda_mesh = bpy.context.active_object
baranda_mesh.name = 'Baranda_Mezzanine'
baranda_mesh.dimensions = (6, 0.05, 0.05)
bpy.ops.object.transform_apply(scale=True)

# Aplicar modificadores
mod_wire = baranda_mesh.modifiers.new(name='Wireframe', type='WIREFRAME')
mod_wire.thickness = 0.01
mod_solidify = baranda_mesh.modifiers.new(name='Solidify', type='SOLIDIFY')
mod_solidify.thickness = 0.01

# Unir todo en un solo objeto
bpy.ops.object.select_all(action='DESELECT')
baranda_mesh.select_set(True)
bpy.context.view_layer.objects.active = baranda_mesh
bpy.ops.object.join()
bpy.context.active_object.name = 'Baranda_Mezzanine'

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(0, -10, 10), energia=3.0)
A.crear_camara('Camara_Principal', ubicacion=(0, -12, 5), rotacion=(80, 0, 0))