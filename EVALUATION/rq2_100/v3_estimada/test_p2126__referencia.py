import blender_arch as A
import bpy

A.limpiar_escena()

# --- Deck y Cimientos con blender_arch ---
deck_ancho = 6.0
deck_fondo = 4.0
deck = A.crear_losa_rectangular('DeckMadera', ancho=deck_ancho, fondo=deck_fondo, espesor=0.15, origen=(0, 0, 0), material='Madera_Roble')
A.crear_losa_rectangular('Cimientos', ancho=deck_ancho+0.2, fondo=deck_fondo+0.2, espesor=0.1, origen=(-0.1, -0.1, -0.1), material='Hormigon')

# --- Pérgola con bpy para estructura personalizada ---
material_pergola = 'Madera_Nogal'
# Postes
poste_seccion = 0.15
poste_alto = 2.5
for i, (x, y) in enumerate([(0.2, 0.2), (deck_ancho - 0.35, 0.2), (0.2, deck_fondo - 0.35), (deck_ancho - 0.35, deck_fondo - 0.35)]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + poste_seccion/2, y + poste_seccion/2, poste_alto/2 + 0.15))
    poste = bpy.context.active_object
    poste.name = f'Poste_Pergola_{i}'
    poste.dimensions = (poste_seccion, poste_seccion, poste_alto)
    A.asignar_material(poste, nombre=material_pergola)

# Vigas
viga_alto = 0.20
for i, y_pos in enumerate([0.2, deck_fondo - 0.35]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(deck_ancho/2, y_pos + poste_seccion/2, poste_alto + 0.15 + viga_alto/2))
    viga = bpy.context.active_object
    viga.name = f'Viga_Principal_{i}'
    viga.dimensions = (deck_ancho, poste_seccion, viga_alto)
    A.asignar_material(viga, nombre=material_pergola)

# Listones transversales
num_listones = 10
for i in range(num_listones):
    x_pos = (deck_ancho / (num_listones - 1)) * i
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, deck_fondo/2, poste_alto + 0.15 + viga_alto + 0.05))
    liston = bpy.context.active_object
    liston.name = f'Liston_{i}'
    liston.dimensions = (0.05, deck_fondo, 0.10)
    A.asignar_material(liston, nombre=material_pergola)

# --- Maceteros de Hormigón con bpy y modificadores ---
macetero_dims = (2.0, 0.5, 0.6)
for i, (x, y) in enumerate([(-macetero_dims[0] - 0.2, 0.5), (deck_ancho + 0.2, deck_fondo - 0.5 - macetero_dims[1])]):
    bpy.ops.mesh.primitive_cube_add(location=(x + macetero_dims[0]/2, y + macetero_dims[1]/2, macetero_dims[2]/2))
    macetero = bpy.context.active_object
    macetero.name = f'Macetero_{i}'
    macetero.dimensions = macetero_dims
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    macetero.modifiers['Solidify'].thickness = -0.08
    bpy.ops.object.modifier_add(type='BEVEL')
    macetero.modifiers['Bevel'].width = 0.01
    A.asignar_material(macetero, nombre='Hormigon')
    A.crear_arbol_simple(f'Arbol_Macetero_{i}', radio_copa=0.8, altura_copa=1.2, altura_tronco=0.5, origen=(x + macetero_dims[0]/2, y + macetero_dims[1]/2, macetero_dims[2]))

A.crear_camara('Camara', ubicacion=(10, -8, 5), rotacion=(70, 0, 40))