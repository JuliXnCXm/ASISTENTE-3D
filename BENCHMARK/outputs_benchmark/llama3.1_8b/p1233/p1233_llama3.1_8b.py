import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el terreno de césped
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
cubierta = bpy.context.active_object
cubierta.name = "Césped"
cubierta.scale = (20, 20, 0.1)

# Crea la casa
bpy.ops.mesh.primitive_cube_add(size=10, location=(0, -9, 2))
casa = bpy.context.active_object
casa.name = "Casa"

# Ajusta las dimensiones de la casa para que sea un rectángulo de 10x8 metros
casa.scale = (10, 8, 5)

# Crea el tejado a dos aguas
bpy.ops.mesh.primitive_plane_add(size=12, location=(0, -4, 7))
techo = bpy.context.active_object
techo.name = "Techo"
techo.scale = (12, 10, 1)
techo.rotation_euler = mathutils.Vector((math.radians(45), 0, 0))

# Ajusta la posición del techo para que esté en el lugar correcto
techo.location = (0, -4, 7)

# Crea los árboles
bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=10, location=(8, -3, 2))
arbol1 = bpy.context.active_object
arbol1.name = "Arbol1"

bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=10, location=(-8, -3, 2))
arbol2 = bpy.context.active_object
arbol2.name = "Arbol2"

# Ajusta la escala de los árboles para que sean más grandes
arbol1.scale = (4, 4, 20)
arbol2.scale = (4, 4, 20)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])