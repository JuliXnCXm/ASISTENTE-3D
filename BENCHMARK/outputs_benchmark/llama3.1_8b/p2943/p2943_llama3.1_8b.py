import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la base de la cubierta
base_length = 12
base_width = 8

# Define las dimensiones de la cumbrera y el espesor
cumbrera_height = 3
espesor = 0.25

# Crea un nuevo objeto para la cubierta a dos aguas
cubierta = bpy.data.objects.new("Cubierta", None)

# Agrega la geometría de la cubierta
bpy.context.collection.objects.link(cubierta)

# Define los vértices de la base de la cubierta
base_vertices = [
    (-base_width/2, -base_length/2, 0),
    (base_width/2, -base_length/2, 0),
    (base_width/2, base_length/2, 0),
    (-base_width/2, base_length/2, 0)
]

# Define los vértices de la cumbrera
cumbrera_vertices = [
    (-base_width/2 + espesor, -base_length/2 + espesor, cumbrera_height),
    (base_width/2 - espesor, -base_length/2 + espesor, cumbrera_height),
    (base_width/2 - espesor, base_length/2 - espesor, cumbrera_height),
    (-base_width/2 + espesor, base_length/2 - espesor, cumbrera_height)
]

# Define los vértices de la parte inferior de la cubierta
inferior_vertices = [
    (-base_width/2 + espesor, -base_length/2 + espesor, 0),
    (base_width/2 - espesor, -base_length/2 + espesor, 0),
    (base_width/2 - espesor, base_length/2 - espesor, 0),
    (-base_width/2 + espesor, base_length/2 - espesor, 0)
]

# Crea un nuevo objeto para la cumbrera
cumbrera = bpy.data.objects.new("Cumbrera", None)

# Agrega la geometría de la cumbrera
bpy.context.collection.objects.link(cumbrera)

# Define los vértices del polígono que forma la cubierta a dos aguas
vertices = base_vertices + cumbrera_vertices + inferior_vertices

# Crea un nuevo objeto para la cubierta a dos aguas
cubierta_a_dos_aguas = bpy.data.objects.new("Cubierta a dos aguas", None)

# Agrega la geometría de la cubierta a dos aguas
bpy.context.collection.objects.link(cubierta_a_dos_aguas)

# Define los polígonos que forman la cubierta a dos aguas
poligonos = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11]
]

# Crea los polígonos que forman la cubierta a dos aguas
for i in range(len(poligonos)):
    bpy.ops.mesh.primitive_polygon_add(vertices=poligonos[i], enter_editmode=False)

# Aplica una transformación de escala para darle forma a la cubierta a dos aguas
bpy.context.object.scale = (base_width, base_length, cumbrera_height)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])