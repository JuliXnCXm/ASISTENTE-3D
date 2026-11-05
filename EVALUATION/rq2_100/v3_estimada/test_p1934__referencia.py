import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y cama base (DSL) ---
ancho, fondo, alto = 4.5, 5, 2.9
hab = A.crear_habitacion('Dormitorio', ancho=ancho, fondo=fondo, alto=alto, material_muro='Muro_Pintura', material_suelo='Parquet')
cama = A.crear_cama('CamaPrincipal', ancho=1.8, largo=2.0, alto_cabecero=1.2, 
                   origen=(ancho/2 - 0.9, 0.2, 0), material_colchon='Textil_Blanco', material_base='Madera_Nogal')

# --- Estructura del dosel (bpy) ---
altura_dosel = 2.4
radio_poste = 0.04

for i in [-1, 1]:
    for j in [0, 1]:
        x = ancho/2 + i * (1.8/2 + radio_poste)
        y = 0.2 + j * (2.0 + 2*radio_poste) - radio_poste
        bpy.ops.mesh.primitive_cylinder_add(radius=radio_poste, depth=altura_dosel, location=(x, y, altura_dosel/2))
        poste = bpy.context.active_object
        poste.name = f'PosteDosel_{i}_{j}'
        A.asignar_material(poste, 'Marco_Negro')

# --- Tela del dosel con simulación de tela (bpy) ---
bpy.ops.mesh.primitive_grid_add(x_subdivisions=50, y_subdivisions=50, size=1, location=(ancho/2, 1.2, altura_dosel + 0.2))
tela = bpy.context.active_object
tela.name = 'TelaDosel'
tela.scale = (2.0, 2.5, 1)
A.asignar_material(tela, 'Textil_Blanco')

# Grupo de vértices para anclar
vg = tela.vertex_groups.new(name='Pinned')
vertices_a_anclar = [v.index for v in tela.data.vertices if v.co[0] > 0.9 or v.co[0] < -0.9]
vg.add(vertices_a_anclar, 1.0, 'REPLACE')

# Modificador de tela
cloth_mod = tela.modifiers.new(name='SimTela', type='CLOTH')
cloth_mod.settings.quality = 5
cloth_mod.settings.mass = 0.1
cloth_mod.settings.vertex_group_mass = 'Pinned'

# Ejecutar simulación (requiere animación)
bpy.context.scene.frame_end = 50
bpy.context.scene.frame_set(50)

# --- Lámpara de pie articulada (bpy) ---
base_lamp = (0.5, fondo - 0.8, 0)
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.05, location=base_lamp)
A.asignar_material(bpy.context.active_object, 'Marco_Negro')

brazo1_loc = (base_lamp[0], base_lamp[1], base_lamp[2] + 0.7)
bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=1.4, location=brazo1_loc)
brazo1 = bpy.context.active_object
brazo1.rotation_euler[1] = 0.5 # Inclinación
A.asignar_material(brazo1, 'Marco_Negro')

brazo2_loc = (brazo1_loc[0] + 0.3, brazo1_loc[1], brazo1_loc[2] + 0.6)
bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.8, location=brazo2_loc)
brazo2 = bpy.context.active_object
brazo2.rotation_euler[1] = -0.8
A.asignar_material(brazo2, 'Marco_Negro')

# --- Iluminación y cámara ---
A.agregar_luz('LuzGeneral', tipo='SUN', ubicacion=(10, -10, 10), energia=3)
A.crear_camara('CamaraDormitorio', ubicacion=(0.5, 5, 1.5), rotacion=(80, 0, 190))