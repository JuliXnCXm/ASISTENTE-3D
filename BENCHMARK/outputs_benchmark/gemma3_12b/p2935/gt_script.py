import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
losa_x, losa_y, losa_z = 4.0, 3.0, 0.15
poste_dim, poste_alto = 0.15, 2.5
viga_alto = 0.2

# Crear Losa
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -losa_z / 2))
losa = bpy.context.active_object
losa.name = 'Losa_Hormigon'
losa.dimensions = (losa_x, losa_y, losa_z)

# Crear un poste de referencia
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, poste_alto / 2))
poste_ref = bpy.context.active_object
poste_ref.name = 'Poste'
poste_ref.dimensions = (poste_dim, poste_dim, poste_alto)

# Ubicar los 4 postes
pos_x = (losa_x - poste_dim) / 2
pos_y = (losa_y - poste_dim) / 2
posiciones_postes = [
    (pos_x, pos_y, poste_alto / 2),
    (-pos_x, pos_y, poste_alto / 2),
    (pos_x, -pos_y, poste_alto / 2),
    (-pos_x, -pos_y, poste_alto / 2)
]

postes = []
for i, pos in enumerate(posiciones_postes):
    nuevo_poste = poste_ref.copy()
    nuevo_poste.data = poste_ref.data.copy()
    nuevo_poste.location = pos
    nuevo_poste.name = f'Poste_{i+1}'
    bpy.context.collection.objects.link(nuevo_poste)
    postes.append(nuevo_poste)
bpy.data.objects.remove(poste_ref)

# Crear Vigas
loc_z_vigas = poste_alto + viga_alto / 2

# Vigas largas (eje X)
viga_larga_dim = (losa_x, poste_dim, viga_alto)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, pos_y, loc_z_vigas))
viga1 = bpy.context.active_object
viga1.name = 'Viga_Larga_1'
viga1.dimensions = viga_larga_dim
viga2 = viga1.copy()
viga2.data = viga1.data.copy()
viga2.location.y = -pos_y
viga2.name = 'Viga_Larga_2'
bpy.context.collection.objects.link(viga2)

# Vigas cortas (eje Y)
viga_corta_dim = (poste_dim, losa_y - poste_dim*2, viga_alto)
bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x, 0, loc_z_vigas))
viga3 = bpy.context.active_object
viga3.name = 'Viga_Corta_1'
viga3.dimensions = viga_corta_dim
viga4 = viga3.copy()
viga4.data = viga3.data.copy()
viga4.location.x = -pos_x
viga4.name = 'Viga_Corta_2'
bpy.context.collection.objects.link(viga4)