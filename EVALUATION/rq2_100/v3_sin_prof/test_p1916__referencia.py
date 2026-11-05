import blender_arch as A
import bpy
import random
import math

A.limpiar_escena()

# --- Entorno de la oficina ---
suelo = A.crear_piso('Suelo_Oficina', ancho=3.5, fondo=3, material='Parquet')
muro_largo = A.crear_muro('Muro_Largo', largo=3.5, alto=2.6, origen=(0,3,0), material='Muro_Pintura')
muro_corto = A.crear_muro('Muro_Corto', largo=3, alto=2.6, origen=(3.5,0,0), rotacion_z=-90, material='Muro_Pintura')

# --- Escritorio en L a medida (bpy) ---
# Parte larga
bpy.ops.mesh.primitive_cube_add(location=(1.25, 2.9, 0.75))
tablero1 = bpy.context.active_object
tablero1.name = 'Escritorio_Tablero1'
tablero1.dimensions = (2.5, 0.6, 0.04)

# Parte corta
bpy.ops.mesh.primitive_cube_add(location=(3.2, 1.5, 0.75))
tablero2 = bpy.context.active_object
tablero2.name = 'Escritorio_Tablero2'
tablero2.dimensions = (0.6, 3.0, 0.04)

# Unir con booleana
mod = tablero2.modifiers.new(name='Union', type='BOOLEAN')
mod.object = tablero1
mod.operation = 'UNION'
bpy.context.view_layer.objects.active = tablero2
bpy.ops.object.modifier_apply(modifier=mod.name)
tablero1.hide_set(True)
A.asignar_material(tablero2, nombre='Madera_Roble')

# --- Estantería con blender_arch ---
estanteria = A.crear_estanteria(
    'Estanteria_Principal', 
    ancho=1.2, alto=2.2, fondo=0.3, num_estantes=5,
    origen=(0.1, 0.1, 0), 
    material='MDF_Blanco'
)

# --- Libros generados proceduralmente (bpy) ---
for i in range(30):
    ancho = random.uniform(0.04, 0.08)
    alto = random.uniform(0.2, 0.3)
    fondo = random.uniform(0.15, 0.2)
    x = random.uniform(0.1 + 0.05, 1.3 - 0.05)
    z = 0.3 + (i // 6) * (2.2 / 5)
    
    bpy.ops.mesh.primitive_cube_add(location=(x, 0.25, z))
    libro = bpy.context.active_object
    libro.name = f'Libro_{i}'
    libro.dimensions = (ancho, fondo, alto)
    color = (random.random(), random.random(), random.random(), 1)
    A.asignar_material(libro, nombre=f'LibroMat_{i}', base_color=color)

# --- Silla de oficina con primitivas (bpy) ---
# Asiento
bpy.ops.mesh.primitive_cube_add(location=(2, 2, 0.45))
asiento = bpy.context.active_object
asiento.dimensions = (0.45, 0.45, 0.05)
A.asignar_material(asiento, nombre='Tela_Gris')
# Respaldo
bpy.ops.mesh.primitive_cube_add(location=(2, 2.22, 0.7))
respaldo = bpy.context.active_object
respaldo.dimensions = (0.45, 0.05, 0.5)
A.asignar_material(respaldo, nombre='Tela_Gris')
# Base
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.4, location=(2, 2, 0.25))
# Ruedas (simplificado)
for i in range(5):
    angle = i * (360/5)
    rad = 0.25
    lx = 2 + rad * math.cos(math.radians(angle))
    ly = 2 + rad * math.sin(math.radians(angle))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.05, location=(lx, ly, 0.05))

# --- Iluminación y cámara ---
A.agregar_luz('Luz_Oficina', tipo='AREA', ubicacion=(1.75, 1.5, 2.5), energia=400)
A.crear_camara('Camara', ubicacion=(-1, -0.5, 1.5), rotacion=(75, 0, -45))