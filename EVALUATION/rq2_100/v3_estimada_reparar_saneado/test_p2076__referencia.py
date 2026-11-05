import blender_arch as A
import bpy
from math import radians

A.limpiar_escena()

# --- ESTRUCTURA Y SOFA (DSL) ---
habitacion = A.crear_habitacion('Sala_Estar', ancho=6, fondo=4, alto=2.8, material_muro='Muro_Pintura', material_suelo='Parquet')
sofa = A.crear_sofa('Sofa_Principal', ancho=2.8, origen=(3, 3.5, 0), material='Tela_Gris')
sofa.rotation_euler[2] = radians(180)

# --- ALFOMBRA PERSONALIZADA (bpy) ---
bpy.ops.mesh.primitive_plane_add(size=1, location=(3, 2, 0.01))
alfombra = bpy.context.active_object
alfombra.name = 'Alfombra'
alfombra.scale = (3.5, 2.5, 1)

# Modificadores para dar grosor y suavizar bordes
mod_solid = alfombra.modifiers.new(name='Grosor', type='SOLIDIFY')
mod_solid.thickness = 0.015
mod_bevel = alfombra.modifiers.new(name='Bisel', type='BEVEL')
mod_bevel.width = 0.01
mod_bevel.segments = 3
A.asignar_material(alfombra, 'Tela_Beige')

# --- ESTANTERIA MODULAR DE DISEÑO (bpy) ---
# Crear el módulo base
ancho_modulo = 0.8
alto_modulo = 0.4
prof_modulo = 0.3
grosor_panel = 0.02

# Panel vertical
bpy.ops.mesh.primitive_cube_add(location=(0.15, 0.15, alto_modulo / 2))
v_panel = bpy.context.active_object
v_panel.scale = (grosor_panel, prof_modulo, alto_modulo)

# Panel horizontal
bpy.ops.mesh.primitive_cube_add(location=(ancho_modulo/2, 0.15, grosor_panel/2))
h_panel = bpy.context.active_object
h_panel.scale = (ancho_modulo, prof_modulo, grosor_panel)

# Unir paneles en un solo objeto módulo
h_panel.select_set(True)
v_panel.select_set(True)
bpy.context.view_layer.objects.active = v_panel
bpy.ops.object.join()
modulo_base = bpy.context.active_object
modulo_base.name = 'Modulo_Estanteria'
A.asignar_material(modulo_base, 'Madera_Nogal')

# Crear la estantería completa usando el módulo
for fila in range(5):
    for col in range(3):
        if (fila + col) % 2 == 0: # Para un patrón alterno
            nueva_pos = (0.5 + col * ancho_modulo, 0, 0.2 + fila * alto_modulo)
            copia_modulo = modulo_base.copy()
            copia_modulo.data = modulo_base.data.copy()
            copia_modulo.location = nueva_pos
            bpy.context.collection.objects.link(copia_modulo)

bpy.data.objects.remove(modulo_base)

A.crear_camara('Camara_Sala', ubicacion=(10, 2, 1.8), rotacion=(radians(80), 0, radians(100)))