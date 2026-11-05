import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA PRINCIPAL CON DSL ---
A.crear_piso('LosaLoft', ancho=8, fondo=6, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')
A.crear_muro('Muro_Fondo', largo=8, alto=4.5, grosor=0.3, origen=(-4,3,0), material='Hormigon')
A.crear_muro('Muro_Frente', largo=8, alto=4.5, grosor=0.3, origen=(-4,-3,0), material='Hormigon')
A.crear_columna('Columna_1', seccion='rect', ancho=0.4, fondo=0.4, alto=4.5, origen=(-2,0,0), material='Hormigon')
A.crear_columna('Columna_2', seccion='rect', ancho=0.4, fondo=0.4, alto=4.5, origen=(2,0,0), material='Hormigon')

# --- MEZZANINE CON MALLA METÁLICA EN BLPY ---
# Crear el volumen del mezzanine
mezzanine_z = 2.5
mezzanine_fondo = 5.5
mezzanine_ancho = 8.0
mezzanine_alto = 0.3
mezzanine_x = 0

# Malla base del mezzanine
verts = [
    (-mezzanine_ancho/2, -mezzanine_fondo/2, mezzanine_z),
    (mezzanine_ancho/2, -mezzanine_fondo/2, mezzanine_z),
    (mezzanine_ancho/2, mezzanine_fondo/2, mezzanine_z),
    (-mezzanine_ancho/2, mezzanine_fondo/2, mezzanine_z),
    (-mezzanine_ancho/2, -mezzanine_fondo/2, mezzanine_z + mezzanine_alto),
    (mezzanine_ancho/2, -mezzanine_fondo/2, mezzanine_z + mezzanine_alto),
    (mezzanine_ancho/2, mezzanine_fondo/2, mezzanine_z + mezzanine_alto),
    (-mezzanine_ancho/2, mezzanine_fondo/2, mezzanine_z + mezzanine_alto)
]
faces = [(0,1,2,3), (4,5,6,7)]
mesh_data = bpy.data.meshes.new('MeshMezzanine')
mesh_data.from_pydata(verts, [], faces)
mez = bpy.data.objects.new('Mezzanine', mesh_data)

# Modificadores para crear la baranda
mod_wire = mez.modifiers.new(name='Wireframe', type='WIREFRAME')
mod_wire.thickness = 0.02
mod_solidify = mez.modifiers.new(name='Solidify', type='SOLIDIFY')
mod_solidify.thickness = 0.01

# Aplicar modificadores y unir a la escena
bpy.context.view_layer.objects.active = mez
bpy.ops.object.modifier_apply(modifier=mod_wire.name)
bpy.ops.object.modifier_apply(modifier=mod_solidify.name)
A.asignar_material(mez, nombre="Acero_Inox", base_color=(0.9, 0.9, 0.9, 1))

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('LuzPrincipal', tipo='AREA', ubicacion=(0,0,4), energia=1500, color=(1,1,1))
A.crear_camara('Camara', ubicacion=(10, -10, 5), rotacion=(75, 0, 45), activa=True)