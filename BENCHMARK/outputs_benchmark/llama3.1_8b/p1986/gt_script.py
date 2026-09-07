import blender_arch as A
import bpy
from math import pi

A.limpiar_escena()

# --- Estructura de la cocina ---
muro_fondo = A.crear_muro('Muro_Fondo', largo=4.5, alto=2.8, origen=(0, 4, 0))
muro_lat = A.crear_muro('Muro_Lateral', largo=4, alto=2.8, origen=(4.5, 4, 0), rotacion_z=-90)
piso = A.crear_piso('Piso_Cocina', ancho=4.5, fondo=4, espesor=0.02, material='Porcelanato')
techo = A.crear_techo_plano('Techo_Cocina', ancho=4.5, fondo=4, espesor=0.2, origen=(0, 0, 2.8))

A.asignar_material(muro_fondo, nombre='Pintura_Gris', base_color=(0.8, 0.8, 0.8, 1))
A.asignar_material(muro_lat, nombre='Pintura_Gris', base_color=(0.8, 0.8, 0.8, 1))

# --- Muebles de cocina con blender_arch ---
# Gabinetes bajos
for i in range(4):
    A.crear_armario(f'Gabinete_Bajo_{i}', ancho=0.9, alto=0.9, fondo=0.6, num_puertas=1, origen=(0.45 + i * 0.9, 3.4, 0), material_cuerpo='MDF_Blanco')

# Gabinetes altos
for i in range(4):
    A.crear_armario(f'Gabinete_Alto_{i}', ancho=0.9, alto=0.7, fondo=0.35, num_puertas=1, origen=(0.45 + i * 0.9, 4, 1.6), material_cuerpo='MDF_Blanco')

# Torre de horno
A.crear_armario('Torre_Horno', ancho=0.6, alto=2.2, fondo=0.6, num_puertas=2, origen=(4.2, 3.4, 0), material_cuerpo='MDF_Blanco')

# --- Isla y campana con bpy ---
# Isla base
isla_base = A.crear_armario('Isla_Base', ancho=2.2, alto=0.9, fondo=1.0, origen=(1.15, 1, 0), material_cuerpo='Madera_Nogal')

# Encimeras
encimera_principal = A.crear_losa_rectangular('Encimera_Principal', ancho=4.5, fondo=0.65, espesor=0.04, origen=(0, 3.35, 0.9), material='Marmol_Blanco')
encimera_isla = A.crear_losa_rectangular('Encimera_Isla', ancho=2.4, fondo=1.2, espesor=0.04, origen=(1.05, 0.9, 0.9), material='Marmol_Blanco')

# Campana extractora de diseño (bpy)
campana_origen = (2.25, 1.5, 1.8)
bpy.ops.mesh.primitive_cube_add(size=1, location=campana_origen)
campana = bpy.context.active_object
campana.name = 'Campana_Cuerpo'
campana.scale = (0.8, 0.5, 0.5)
bpy.ops.object.transform_apply(scale=True)
A.asignar_material(campana, nombre='Acero_Inox', base_color=(0.8, 0.8, 0.8, 1))

# Suspensión de la campana
bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=1.0, location=(campana_origen[0], campana_origen[1], campana_origen[2] + 0.75))
suspension = bpy.context.active_object
suspension.name = 'Campana_Suspension'
A.asignar_material(suspension, nombre='Acero_Inox', base_color=(0.8, 0.8, 0.8, 1))

# --- Iluminación ---
A.agregar_luz('Luz_Isla', tipo='AREA', ubicacion=(2.25, 1.5, 2.6), energia=200, color=(1, 0.9, 0.8))
luz_area = bpy.data.lights['Luz_Isla']
luz_area.shape = 'RECTANGLE'
luz_area.size = 1.5
luz_area.size_y = 0.8