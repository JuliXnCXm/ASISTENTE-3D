import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la pérgola
ancho = 4
alto = 3
altura = 2.5

# Crea las columnas
for i in range(4):
    columna = bpy.data.curves.new(name="Columna", type='MESH')
    objeto = bpy.data.objects.new("Columna" + str(i), columna)
    bpy.context.collection.objects.link(objeto)

    # Define la posición de la columna
    if i == 0:
        x, y, z = -ancho/2, 0, 0
    elif i == 1:
        x, y, z = ancho/2, 0, 0
    elif i == 2:
        x, y, z = 0, -alto, 0
    else:
        x, y, z = 0, alto, 0

    # Establece la posición de la columna
    objeto.location = mathutils.Vector((x, y, z))

    # Define el tamaño de la columna
    columna.data.uv_textures.clear()
    columna.data.vertices.add(4)
    columna.data.polygons.add(4)

    # Define las coordenadas de los vértices de la columna
    columna.data.vertices[0].co = (x - 0.1, y + 0.1, z)
    columna.data.vertices[1].co = (x + 0.1, y + 0.1, z)
    columna.data.vertices[2].co = (x + 0.1, y - 0.1, z)
    columna.data.vertices[3].co = (x - 0.1, y - 0.1, z)

    # Define las coordenadas de los lados de la columna
    columna.data.polygons[0].vertices = (0, 1, 2)
    columna.data.polygons[0].normal = mathutils.Vector((0, 0, 1))
    columna.data.polygons[0].use_smooth = True

    columna.data.polygons[1].vertices = (1, 2, 3)
    columna.data.polygons[1].normal = mathutils.Vector((0, 0, -1))
    columna.data.polygons[1].use_smooth = True

    columna.data.polygons[2].vertices = (0, 1, 3)
    columna.data.polygons[2].normal = mathutils.Vector((1, 0, 0))
    columna.data.polygons[2].use_smooth = True

    columna.data.polygons[3].vertices = (0, 2, 3)
    columna.data.polygons[3].normal = mathutils.Vector((-1, 0, 0))
    columna.data.polygons[3].use_smooth = True

# Crea el techo
techo = bpy.data.curves.new(name="Techo", type='MESH')
objeto_techo = bpy.data.objects.new("Techo", techo)
bpy.context.collection.objects.link(objeto_techo)

# Define la posición del techo
x, y, z = 0, alto, altura

# Establece la posición del techo
objeto_techo.location = mathutils.Vector((x, y, z))

# Define el tamaño del techo
techo.data.uv_textures.clear()
techo.data.vertices.add(4)
techo.data.polygons.add(4)

# Define las coordenadas de los vértices del techo
techo.data.vertices[0].co = (x - ancho/2, y + alto/2, z)
techo.data.vertices[1].co = (x + ancho/2, y + alto/2, z)
techo.data.vertices[2].co = (x + ancho/2, y - alto/2, z)
techo.data.vertices[3].co = (x - ancho/2, y - alto/2, z)

# Define las coordenadas de los lados del techo
techo.data.polygons[0].vertices = (0, 1, 2)
techo.data.polygons[0].normal = mathutils.Vector((0, 0, 1))
techo.data.polygons[0].use_smooth = True

techo.data.polygons[1].vertices = (1, 2, 3)
techo.data.polygons[1].normal = mathutils.Vector((0, 0, -1))
techo.data.polygons[1].use_smooth = True

techo.data.polygons[2].vertices = (0, 1, 3)
techo.data.polygons[2].normal = mathutils.Vector((1, 0, 0))
techo.data.polygons[2].use_smooth = True

techo.data.polygons[3].vertices = (0, 2, 3)
techo.data.polygons[3].normal = mathutils.Vector((-1, 0, 0))
techo.data.polygons[3].use_smooth = True

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])