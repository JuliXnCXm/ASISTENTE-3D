import blender_arch as A
import bpy
import math

A.limpiar_escena()

# --- Base de la plaza y vegetación con blender_arch ---
plaza_ancho = 15.0
plaza_fondo = 12.0
A.crear_piso('Suelo_Plaza', ancho=plaza_ancho, fondo=plaza_fondo, espesor=0.1, origen=(0, 0, 0), material='Porcelanato')
A.crear_arbol_simple('Arbol_1', origen=(1, 1, 0))
A.crear_arbol_simple('Arbol_2', radio_copa=2.0, origen=(plaza_ancho - 2, plaza_fondo - 2.5, 0))
A.crear_arbol_simple('Arbol_3', origen=(1, plaza_fondo - 2.5, 0))

# --- Fuente central con bpy ---
centro_x, centro_y = plaza_ancho / 2, plaza_fondo / 2
# Base
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=2.5, depth=0.3, location=(centro_x, centro_y, 0.15))
A.asignar_material(bpy.context.active_object, nombre='Hormigon')
# Segundo nivel
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.5, depth=0.4, location=(centro_x, centro_y, 0.3 + 0.2))
A.asignar_material(bpy.context.active_object, nombre='Hormigon')
# Tercer nivel (surtidor)
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.5, depth=0.8, location=(centro_x, centro_y, 0.5 + 0.4))
surtidor = bpy.context.active_object
A.asignar_material(surtidor, nombre='Hormigon')

# Agua con bpy
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=2.45, depth=0.05, location=(centro_x, centro_y, 0.28))
A.asignar_material(bpy.context.active_object, nombre='Agua')
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.45, depth=0.05, location=(centro_x, centro_y, 0.68))
A.asignar_material(bpy.context.active_object, nombre='Agua')

# --- Bancos de diseño personalizado con bpy ---
num_bancos = 4
radio_bancos = 4.5
for i in range(num_bancos):
    angulo = (math.pi * 2 / num_bancos) * i
    x = centro_x + radio_bancos * math.cos(angulo)
    y = centro_y + radio_bancos * math.sin(angulo)
    
    # Asiento
    bpy.ops.mesh.primitive_cube_add(location=(x, y, 0.45))
    asiento = bpy.context.active_object
    asiento.name = f'Asiento_Banco_{i}'
    asiento.dimensions = (1.8, 0.4, 0.1)
    asiento.rotation_euler[2] = angulo
    A.asignar_material(asiento, nombre='Madera')
    
    # Soportes
    for j in [-0.7, 0.7]:
        offset_x = j * math.cos(angulo)
        offset_y = j * math.sin(angulo)
        bpy.ops.mesh.primitive_cube_add(location=(x + offset_x, y + offset_y, 0.2))
        soporte = bpy.context.active_object
        soporte.name = f'Soporte_Banco_{i}_{j}'
        soporte.dimensions = (0.1, 0.4, 0.4)
        soporte.rotation_euler[2] = angulo
        A.asignar_material(soporte, nombre='Acero_Inox')

A.agregar_luz('Sol', tipo='SUN', ubicacion=(5, -5, 10), energia=3)
A.crear_camara('Camara', ubicacion=(16, -10, 8))