import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
base_largo = 10.0 # en X
base_ancho = 6.0  # en Y
altura_cumbrera = 2.0
espesor = 0.20

# Definir vértices de la forma base (prisma triangular)
verts = [
    (-base_largo/2, -base_ancho/2, 0), # 0
    (base_largo/2, -base_ancho/2, 0),  # 1
    (base_largo/2, base_ancho/2, 0),   # 2
    (-base_largo/2, base_ancho/2, 0),  # 3
    (-base_largo/2, 0, altura_cumbrera), # 4 Cumbrera
    (base_largo/2, 0, altura_cumbrera)   # 5 Cumbrera
]

# Definir caras usando los índices de los vértices
faces = [
    (0, 1, 5, 4), # Faldón 1
    (1, 2, 2, 1), # Tímpano 1 (inválido, se corrige) -> (1,2,5)
    (2, 3, 4, 5), # Faldón 2
    (3, 0, 4, 3), # Tímpano 2 (inválido, se corrige) -> (3,0,4)
]
# Corregir caras para que sean polígonos válidos
faces_correctas = [
    (0, 1, 5, 4), # Faldón 1
    (2, 3, 4, 5), # Faldón 2
    (0, 3, 4),    # Tímpano frontal
    (1, 2, 5)     # Tímpano trasero
]

# Crear la malla y el objeto
mesh_data = bpy.data.meshes.new('CubiertaMesh')
mesh_data.from_pydata(verts, [], faces_correctas)
mesh_data.update()

obj = bpy.data.objects.new('CubiertaDosAguas', mesh_data)

# Añadir el objeto a la escena
scene = bpy.context.scene
scene.collection.objects.link(obj)

# Aplicar modificador de grosor
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

solidify_mod = obj.modifiers.new(name='EspesorLosa', type='SOLIDIFY')
solidify_mod.thickness = espesor
solidify_mod.offset = 1