import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la habitación
ancho = 5
alto = 4
altura = 2.7
espesor_pared = 0.15

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=ancho, location=(0, 0, -altura))
suelo = bpy.context.active_object
suelo.name = "Suelo"
suelo.scale = (ancho, alto, 1)

# Crea las paredes
pared_lateral_derecha = bpy.ops.mesh.primitive_cube_add(size=alto, location=(ancho/2 + espesor_pared, 0, -altura))
bpy.context.active_object.name = "Pared Lateral Derecha"
bpy.context.active_object.scale = (espesor_pared, alto, altura)
pared_lateral_izquierda = bpy.ops.mesh.primitive_cube_add(size=alto, location=(-ancho/2 - espesor_pared, 0, -altura))
bpy.context.active_object.name = "Pared Lateral Izquierda"
bpy.context.active_object.scale = (espesor_pared, alto, altura)
pared_frente = bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, ancho/2 + espesor_pared, -altura))
bpy.context.active_object.name = "Pared Frente"
bpy.context.active_object.scale = (ancho, espesor_pared, altura)
pared_atras = bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, -ancho/2 - espesor_pared, -altura))
bpy.context.active_object.name = "Pared Atras"
bpy.context.active_object.scale = (ancho, espesor_pared, altura)

# Crea el techo
bpy.ops.mesh.primitive_plane_add(size=ancho, location=(0, 0, altura))
techo = bpy.context.active_object
techo.name = "Techo"
techo.scale = (ancho, alto, 1)
techo.location = (0, 0, altura)

# Crea la cama simple
cama_simple = bpy.ops.mesh.primitive_cube_add(size=2.5, location=(0, -1.75, -altura + 1))
bpy.context.active_object.name = "Cama Simple"
bpy.context.active_object.scale = (2.5, 2.5, 0.5)

# Crea la mesa de noche
mesa_noche = bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, -1.75, -altura + 1))
bpy.context.active_object.name = "Mesa Noche"
bpy.context.active_object.scale = (1.5, 1.5, 0.5)

# Guarda el archivo .blend si se especificó la ruta
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])