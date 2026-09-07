import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la pérgola
ancho = 4
alto = 3
profundidad = 2.5

# Crea los postes en las esquinas
for i in range(4):
    x, y, z = (0, 0, 0), (ancho, 0, 0), (0, alto, 0), (ancho, alto, 0)
    if i == 0:
        x, y = (0, 0, 0), (ancho/2 - 0.1, 0, 0)
    elif i == 1:
        x, y = (ancho, 0, 0), (ancho + ancho/2 - 0.1, 0, 0)
    elif i == 2:
        x, y = (0, alto, 0), (ancho/2 - 0.1, alto, 0)
    else:
        x, y = (ancho, alto, 0), (ancho + ancho/2 - 0.1, alto, 0)

    bpy.ops.mesh.primitive_cube_add(size=profundidad, location=x, rotation=(mathutils.Matrix.Rotation(math.radians(90), 4)))
    post = bpy.context.active_object
    post.scale = (0.2, 0.2, profundidad)
    post.name = f"Poste {i+1}"

# Crea las vigas principales
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(ancho/2 - ancho/4, alto/2, 0), rotation=(mathutils.Matrix.Rotation(math.radians(90), 4)))
viga_principal = bpy.context.active_object
viga_principal.scale = (ancho, 0.1, profundidad)
viga_principal.name = "Viga Principal"

bpy.ops.mesh.primitive_cube_add(size=ancho, location=(-ancho/2 + ancho/4, alto/2, 0), rotation=(mathutils.Matrix.Rotation(math.radians(90), 4)))
viga_principal = bpy.context.active_object
viga_principal.scale = (ancho, 0.1, profundidad)
viga_principal.name = "Viga Principal"

# Crea las vigas transversales
for i in range(5):
    x, y, z = (-ancho/2 + ancho/4, alto/2 - 0.05 * (i+1), 0), (ancho/2 - ancho/4, alto/2 - 0.05 * (i+1), 0)
    bpy.ops.mesh.primitive_cube_add(size=profundidad, location=x, rotation=(mathutils.Matrix.Rotation(math.radians(90), 4)))
    viga_transversal = bpy.context.active_object
    viga_transversal.scale = (ancho/2 - ancho/8, 0.1, profundidad)
    viga_transversal.name = f"Viga Transversal {i+1}"

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])