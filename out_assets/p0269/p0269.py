import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configuración de escena
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 10.0
ancho = 6.0
altura_cumbrera = 2.5
espesor = 0.2

# Vértices de la cubierta (sin espesor)
verts = [
    (-largo / 2, -ancho / 2, 0),  # 0: Alero frontal izquierdo
    (largo / 2, -ancho / 2, 0),   # 1: Alero frontal derecho
    (largo / 2, ancho / 2, 0),    # 2: Alero trasero derecho
    (-largo / 2, ancho / 2, 0),   # 3: Alero trasero izquierdo
    (-largo / 2, 0, altura_cumbrera), # 4: Cumbrera izquierda
    (largo / 2, 0, altura_cumbrera)   # 5: Cumbrera derecha
]

# Caras que conectan los vértices
faces = [
    (0, 1, 5, 4),  # Faldón frontal
    (2, 3, 4, 5)   # Faldón trasero
]

# Crear la malla y el objeto
mesh_data = bpy.data.meshes.new("CubiertaMesh")
mesh_data.from_pydata(verts, [], faces)
mesh_data.update()

obj_cubierta = bpy.data.objects.new("CubiertaDosAguas", mesh_data)

# Añadir el objeto a la escena
bpy.context.collection.objects.link(obj_cubierta)

# Aplicar modificador de solidificar para dar espesor
bpy.context.view_layer.objects.active = obj_cubierta
mod = obj_cubierta.modifiers.new(name="Solidify", type='SOLIDIFY')
mod.thickness = espesor