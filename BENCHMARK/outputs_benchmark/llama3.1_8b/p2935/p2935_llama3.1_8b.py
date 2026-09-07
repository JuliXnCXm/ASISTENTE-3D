import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la losa y la pérgola
lado_losa = 4.0
ancho_losa = 3.0
espacio_losa = 0.15

alto_pergola = 2.5
ancho_poste = 0.15

# Crea la losa de hormigón
bpy.ops.mesh.primitive_cube_add(size=ancho_losa, location=(lado_losa/2, ancho_losa/2, 0))
objeto_losa = bpy.context.active_object
objeto_losa.scale = (lado_losa, ancho_losa, espacio_losa)

# Crea los postes verticales cuadrados en las esquinas
for i in range(4):
    x = lado_losa/2 + (ancho_losa - ancho_poste)/2 if i % 2 == 0 else -lado_losa/2 - (ancho_losa - ancho_poste)/2
    y = ancho_losa/2 + (ancho_losa - ancho_poste)/2 if i < 2 else -ancho_losa/2 - (ancho_losa - ancho_poste)/2
    bpy.ops.mesh.primitive_cube_add(size=ancho_poste, location=(x, y, alto_pergola))
    objeto_poste = bpy.context.active_object
    objeto_poste.scale = (ancho_poste, ancho_poste, alto_pergola)

# Crea las vigas horizontales conectando los postes en la parte superior
for i in range(4):
    x = lado_losa/2 + (ancho_losa - ancho_poste)/2 if i % 2 == 0 else -lado_losa/2 - (ancho_losa - ancho_poste)/2
    y = ancho_losa/2 + (ancho_losa - ancho_poste)/2 if i < 2 else -ancho_losa/2 - (ancho_losa - ancho_poste)/2
    bpy.ops.mesh.primitive_cube_add(size=ancho_poste, location=(x, y, alto_pergola + ancho_poste))
    objeto_viga = bpy.context.active_object
    objeto_viga.scale = (ancho_poste, ancho_poste, ancho_poste)

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])