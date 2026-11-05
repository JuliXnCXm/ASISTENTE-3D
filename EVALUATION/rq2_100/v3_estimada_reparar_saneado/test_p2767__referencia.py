import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones generales
largo_pergola = 4.0
ancho_pergola = 3.0
alto_pergola = 2.8

# Dimensiones elementos constructivos
dim_poste = (0.15, 0.15, alto_pergola)
dim_viga = (largo_pergola, 0.15, 0.20)
dim_vigueta = (0.10, ancho_pergola + 0.4, 0.15) # +0.4 para que sobresalgan
num_viguetas = 5

# Colección para la pérgola
coleccion_pergola = bpy.data.collections.new('Pergola')
bpy.context.scene.collection.children.link(coleccion_pergola)

# --- 1. Crear Postes ---
pos_x = (largo_pergola - dim_poste[0]) / 2
pos_y = (ancho_pergola - dim_poste[1]) / 2
posiciones_postes = [
    (pos_x, pos_y, alto_pergola / 2),
    (-pos_x, pos_y, alto_pergola / 2),
    (pos_x, -pos_y, alto_pergola / 2),
    (-pos_x, -pos_y, alto_pergola / 2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(location=pos)
    poste = bpy.context.active_object
    poste.name = f'Poste_{i+1}'
    poste.dimensions = dim_poste
    bpy.ops.object.transform_apply(scale=True)
    coleccion_pergola.objects.link(poste)
    bpy.context.scene.collection.objects.unlink(poste)

# --- 2. Crear Vigas Principales ---
pos_y_viga = (ancho_pergola - dim_viga[1]) / 2
pos_z_viga = alto_pergola + dim_viga[2] / 2
posiciones_vigas = [
    (0, pos_y_viga, pos_z_viga),
    (0, -pos_y_viga, pos_z_viga)
]
for i, pos in enumerate(posiciones_vigas):
    bpy.ops.mesh.primitive_cube_add(location=pos)
    viga = bpy.context.active_object
    viga.name = f'Viga_Principal_{i+1}'
    viga.dimensions = dim_viga
    bpy.ops.object.transform_apply(scale=True)
    coleccion_pergola.objects.link(viga)
    bpy.context.scene.collection.objects.unlink(viga)

# --- 3. Crear Viguetas Transversales ---
espaciado_viguetas = largo_pergola / (num_viguetas - 1)
pos_z_vigueta = alto_pergola + dim_viga[2] + dim_vigueta[2] / 2

for i in range(num_viguetas):
    pos_x_vigueta = -largo_pergola / 2 + i * espaciado_viguetas
    bpy.ops.mesh.primitive_cube_add(location=(pos_x_vigueta, 0, pos_z_vigueta))
    vigueta = bpy.context.active_object
    vigueta.name = f'Vigueta_{i+1}'
    vigueta.dimensions = dim_vigueta
    bpy.ops.object.transform_apply(scale=True)
    coleccion_pergola.objects.link(vigueta)
    bpy.context.scene.collection.objects.unlink(vigueta)