import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA PRINCIPAL ---
A.crear_terreno_plano('Suelo_Jardin', ancho=12, fondo=12, espesor=0.2, material='Cesped')
A.crear_columna('Columna_1', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(-3, -3, 0), material='Madera_Roble')
A.crear_columna('Columna_2', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(3, -3, 0), material='Madera_Roble')

# Vigas principales
A.crear_losa_rectangular('Viga_Principal_1', ancho=10, fondo=0.2, espesor=0.2, origen=(-4.5, -3.1, 2.8), material='Madera_Roble')
A.crear_losa_rectangular('Viga_Principal_2', ancho=10, fondo=0.2, espesor=0.2, origen=(4.5, -3.1, 2.8), material='Madera_Roble')

# Vigas secundarias con bisel
def crear_viga_biselada(nombre, largo, origen):
    # Crear la viga base
    A.crear_losa_rectangular(f'{nombre}_Base', ancho=largo, fondo=0.2, espesor=0.2, origen=origen, material='Madera_Roble')
    
    # Crear el bisel
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.1))
    bisel = bpy.context.active_object
    bisel.name = f'Bisel_{nombre}'
    bisel.scale = (largo/2, 0.05, 0.2)
    A.asignar_material(bisel, nombre='Madera_Roble_Bisel')
    
    # Unir y aplicar modificador booleano
    mod = bisel.modifiers.new(name='Boolean', type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = A.obtener_objeto(nombre=f'{nombre}_Base')
    bpy.context.view_layer.objects.active = bisel
    bpy.ops.object.modifier_apply(modifier=mod.name)
    A.asignar_material(bisel, nombre='Madera_Roble')
    A.ocultar_objeto(bisel)

crear_viga_biselada('Viga_Secundaria_1', largo=8, origen=(-3.5, -3.1, 2.8))
crear_viga_biselada('Viga_Secundaria_2', largo=8, origen=(3.5, -3.1, 2.8))

# --- CELOSÍA CON MODIFICADORES ---
# Malla base
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 2.9))
malla_base = bpy.context.active_object
malla_base.name = 'Malla_Celosia'
malla_base.dimensions = (10, 0.05, 0.05)
A.asignar_material(malla_base, nombre='Madera_Roble')

# Modificadores Array y Wireframe
mod_array = malla_base.modifiers.new(name='Array', type='ARRAY')
mod_array.count = 10
mod_array.relative_offset_displace[0] = 1.0
mod_array.use_relative_offset = False
mod_array.use_constant_offset = True
mod_array.constant_offset_displace[0] = 1.0

mod_wire = malla_base.modifiers.new(name='Wireframe', type='WIREFRAME')
mod_wire.thickness = 0.02
mod_wire.wireframes = True
mod_wire.use_vertices = True

# Crear losa superior
A.crear_losa_rectangular('Losa_Celosia', ancho=10, fondo=10, espesor=0.1, origen=(0, 0, 3.0), material='Madera_Roble')

# --- VEGETACIÓN ---
for i in range(12):
    x = -3 + 4 * (i % 4) + 0.5
    z = 2.8 + 0.5
    A.crear_esfera(f'Vegetacion_{i}', radio=0.3, origen=(x, -3, z), material='Hoja')