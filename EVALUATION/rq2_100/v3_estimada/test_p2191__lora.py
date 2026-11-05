import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA PRINCIPAL ---
A.crear_terreno_plano('Suelo_Pergola', ancho=10, fondo=10, material='Cesped')
A.crear_columna('Columna_1', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(-4, -4, 0), material='Madera_Roble')
A.crear_columna('Columna_2', seccion='rect', ancho=0.2, fondo=0.2, alto=2.8, origen=(4, -4, 0), material='Madera_Roble')

# Vigas principales
A.crear_losa_rectangular('Viga_Principal_1', ancho=9.6, fondo=0.2, espesor=0.2, origen=(-4.8, -4.9, 2.8), material='Madera_Roble')
A.crear_losa_rectangular('Viga_Principal_2', ancho=9.6, fondo=0.2, espesor=0.2, origen=(4.8, -4.9, 2.8), material='Madera_Roble')

# Vigas secundarias con bisel
def crear_viga_secundaria(nombre, origen):
    bpy.ops.mesh.primitive_cube_add(location=origen)
    viga = bpy.context.active_object
    viga.name = nombre
    viga.dimensions = (0.2, 0.2, 2.8)
    A.asignar_material(viga, 'Madera_Roble')
    # Crear bisel
    mod_bisel = viga.modifiers.new(name='Bisel', type='BEVEL')
    mod_bisel.width = 0.05
    mod_bisel.segments = 3
    return viga

crear_viga_secundaria('Viga_Secundaria_1', (-4.8, 0, 2.8))
crear_viga_secundaria('Viga_Secundaria_2', (4.8, 0, 2.8))

# --- CELOSÍA CON MODIFICADORES ---
# Malla base
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 2.8 + 0.1))
malla_base = bpy.context.active_object
malla_base.name = 'Malla_Celosia'
malla_base.dimensions = (9.6, 9.6, 0.05)

# Modificador Array para filas
mod_array_filas = malla_base.modifiers.new(name='Array_Filas', type='ARRAY')
mod_array_filas.count = 10
mod_array_filas.relative_offset_displace[0] = 0.96 / 9

# Modificador Wireframe para dar forma
mod_wireframe = malla_base.modifiers.new(name='Wireframe', type='WIREFRAME')
mod_wireframe.thickness = 0.02
mod_wireframe.use_even_offset = True

# Crear huecos
for i in range(10):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array_filas.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(modifier=mod_wireframe.name)
    bpy.ops.object.modifier_apply(modifier=mod_array