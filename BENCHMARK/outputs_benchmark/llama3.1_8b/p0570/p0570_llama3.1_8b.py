import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del edificio
ancho = 20
alto = 15
num_pisos = 5

# Crea el cuerpo del edificio
edificio = bpy.data.objects.new("Edificio", None)
edificio.location = mathutils.Vector((0, 0, 0))
bpy.context.collection.objects.link(edificio)

# Crea la geometría del edificio
for i in range(num_pisos):
    # Crea el piso actual
    piso = bpy.data.objects.new(f"Piso {i+1}", None)
    piso.location = mathutils.Vector((0, 0, i * alto))
    bpy.context.collection.objects.link(piso)

    # Crea la fachada del piso actual
    fachada = bpy.data.meshes.new("Fachada")
    fachada.from_pydata([
        (-ancho/2, -alto/2, i * alto),
        (ancho/2, -alto/2, i * alto),
        (ancho/2, alto/2, i * alto),
        (-ancho/2, alto/2, i * alto)
    ], [], [])
    fachada.update(calc_edges=True)

    # Crea la retícula de ventanas
    ventanas = bpy.data.meshes.new("Ventanas")
    ventanas.from_pydata([
        (-ancho/4, -alto/4, i * alto),
        (ancho/4, -alto/4, i * alto),
        (ancho/4, alto/4, i * alto),
        (-ancho/4, alto/4, i * alto)
    ], [], [])
    ventanas.update(calc_edges=True)

    # Aplica la materiales a las geometrías
    fachada.materials.append(bpy.data.materials.new("Muro Cortina"))
    ventanas.materials.append(bpy.data.materials.new("Ventana"))

    # Asigna las geometrías al piso actual
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.collection.objects.link(fachada)
    bpy.context.collection.objects.link(ventanas)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])