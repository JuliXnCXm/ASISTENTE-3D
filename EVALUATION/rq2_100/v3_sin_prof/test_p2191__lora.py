import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA PRINCIPAL ---
A.crear_terreno_plano('Suelo_Jardin', ancho=12, fondo=8, espesor=0.2, material='Cesped')
A.crear_columna('Columna_1', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(-3, -3, 0), material='Madera_Roble')
A.crear_columna('Columna_2', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(3, -3, 0), material='Madera_Roble')

# Vigas principales
A.extruir_perfil('Viga_Principal', puntos_2d=[(0,0), (6,0), (6,0.2), (0,0.2)], altura=0.2, material='Madera_Roble')
viga1 = A.crear_prisma('Viga_1', largo=6, alto=0.2, prof=0.2, origen=(-3, -3, 2.8))
viga2 = A.crear_prisma('Viga_2', largo=6, alto=0.2, prof=0.2, origen=(3, -3, 2.8))

# --- VIGAS PERSONALIZADAS CON MODIFICADORES ---
# Crear la forma base de la viga
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=0.2, location=(0, 0, 2.8))
base_viga = bpy.context.active_object
base_viga.name = 'Base_Viga_Biselada'

# Crear el biselador
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.1))
biselador = bpy.context.active_object
biselador.name = 'Biselador'
biselador.dimensions = (0.05, 0.05, 0.2)

# Aplicar modificador Bisel
mod_bisel = base_viga.modifiers.new(name='Bisel', type='BEVEL')
mod_bisel.width = 0.02
mod_bisel.segments = 3
mod_bisel.relative_offset_displace[0] = 0.05 # Extremo 1
mod_bisel.relative_offset_displace[1] = 0.05 # Extremo 2

# Crear la viga biselada
bpy.context.view_layer.objects.active = base_viga
bpy.ops.object.modifier_apply(modifier=mod_bisel.name)
biseleada = base_viga.copy()
biseleada.data = base_viga.data.copy()
biseleada.name = 'Viga_Biselada'
A.asignar_material(biseleada, nombre='Madera_Roble', base_color=(0.2, 0.4, 0.2, 1))

# Repetir la viga con un modificador Array
array_mod = biseleada.modifiers.new(name='Array_Vigas', type='ARRAY')
array_mod.count = 11
array_mod.relative_offset_displace[0] = 0.5
array_mod.use_relative_offset = False
array_mod.use_constant_offset = True
array_mod.constant_offset_displace[0] = 0.5

# --- CELOSÍA CON MODIFICADORES ---
# Crear el primer panel de celosía
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 2.8 + 0.2))
panel = bpy.context.active_object
panel.name = 'Panel_Celosia'
panel.dimensions = (0.05, 0.05, 0.05)
panel.rotation_euler[0] = 1.5708 # 90 grados

# Aplicar modificador Wireframe
mod_wire = panel.modifiers.new(name='Wireframe', type='WIREFRAME')
mod_wire.thickness = 0.01
mod_wire.wireframes = True
mod_wire.use_vertices = True

# Crear la celosía
bpy.context.view_layer.objects.active = panel
bpy.ops.object.modifier_apply(modifier=mod_wire.name)
celosia = panel.copy()
celosia.data = panel.data.copy()
celosia.name = 'Celosia'
A.asignar_material(celosia, nombre='Marco_Negro', base_color=(0, 0, 0, 1))

# Repetir la celosía con un modificador Array
array_mod_celosia = celosia.modifiers.new(name='Array_Celosia', type='ARRAY')
array_mod_celosia.count = 11
array_mod_celosia.relative_offset_displace[0] = 0.5
array_mod_celosia.use_relative_offset = False
array_mod_celosia.use_constant_offset = True
array_mod_celosia.constant_offset_displace[0] = 0.5

# --- VEGETACIÓN ---
# Crear esferas para simular árboles
for i in range(12):
    x = -3 + 3 * (i % 4) + 0.5
    z = 0.5 + (i // 4) * 2
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(x, 0, z))
    arbol = bpy.context.active_object
    arbol.name = f'Arbol_{i}'
    A.asignar_material(arbol, nombre='Hoja', base_color=(0.2, 0.6, 0.1, 1))