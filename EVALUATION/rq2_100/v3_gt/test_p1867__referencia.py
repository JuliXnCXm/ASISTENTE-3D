import blender_arch as A
import bpy
from math import radians

A.limpiar_escena()

# --- 1. Contenedor y estantería con blender_arch ---
A.crear_habitacion('Oficina', ancho=4, fondo=3.5, alto=2.6, material_suelo='Concreto_Piso', material_muro='Muro_Pintura')
A.crear_estanteria('Estanteria_Libros', ancho=1.2, alto=2.2, fondo=0.3, num_estantes=5, origen=(0.2, 1.8, 0), material='Madera_Roble')

# --- 2. Escritorio en L personalizado con bpy ---
# Crear las dos partes del escritorio
bpy.ops.mesh.primitive_cube_add(location=(1.25, 3.1, 0.725))
parte1 = bpy.context.active_object
parte1.name = 'Escritorio_Lado_A'
parte1.dimensions = (1.5, 0.6, 0.05)

bpy.ops.mesh.primitive_cube_add(location=(2.3, 2.2, 0.725))
parte2 = bpy.context.active_object
parte2.name = 'Escritorio_Lado_B'
parte2.dimensions = (0.6, 2.0, 0.05)

# Unir las dos partes con un booleano
mod = parte1.modifiers.new(name='Union', type='BOOLEAN')
mod.object = parte2
mod.operation = 'UNION'
bpy.context.view_layer.objects.active = parte1
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(parte2, do_unlink=True)
A.asignar_material(parte1, 'MDF_Blanco')

# --- 3. Silla de oficina ergonómica con bpy ---
# Crear una colección para la silla
silla_collection = bpy.data.collections.new('Coleccion_Silla')
bpy.context.scene.collection.children.link(silla_collection)

# Base con ruedas
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.4, location=(1.5, 1.5, 0.2))
base_central = bpy.context.active_object
base_central.name = 'Base_Cilindro'
silla_collection.objects.link(base_central)

for i in range(5):
    bpy.ops.mesh.primitive_cube_add(scale=(0.35, 0.04, 0.04), location=(1.5, 1.5, 0.04))
    pata = bpy.context.active_object
    pata.name = f'Pata_{i}'
    pata.rotation_euler[2] = radians(i * 72)
    pata.location.x += 0.35/2 * bpy.context.scene.unit_settings.scale_length
    bpy.ops.transform.rotate(value=radians(i * 72), orient_axis='Z', center_override=(1.5, 1.5, 0.04))
    silla_collection.objects.link(pata)

# Asiento
bpy.ops.mesh.primitive_cube_add(location=(1.5, 1.5, 0.45))
asiento = bpy.context.active_object
asiento.name = 'Asiento'
asiento.dimensions = (0.5, 0.5, 0.08)
silla_collection.objects.link(asiento)

# Respaldo
bpy.ops.mesh.primitive_cube_add(location=(1.5, 1.75, 0.8))
respaldo = bpy.context.active_object
respaldo.name = 'Respaldo'
respaldo.dimensions = (0.45, 0.07, 0.6)
respaldo.rotation_euler[0] = radians(10)
silla_collection.objects.link(respaldo)

# Aplicar materiales y modificadores de suavizado
for obj in silla_collection.objects:
    A.asignar_material(obj, nombre='Plastico_Negro', base_color=(0.1,0.1,0.1,1))
    if 'Pata' not in obj.name:
        mod_bevel = obj.modifiers.new(name='Bisel', type='BEVEL')
        mod_bevel.width = 0.02
        mod_bevel.segments = 3
        if 'Asiento' in obj.name or 'Respaldo' in obj.name:
             A.asignar_material(obj, nombre='Textil_Silla', base_color=(0.2,0.25,0.3,1))

# Limpiar coleccion de escena principal
for obj in silla_collection.objects:
    bpy.context.scene.collection.objects.unlink(obj)

A.agregar_luz('Luz_Oficina', ubicacion=(2, 1.75, 3), energia=150)