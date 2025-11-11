import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
pergola_largo = 4.0
pergola_ancho = 3.0
poste_alto = 2.5
poste_lado = 0.15
viga_alto = 0.20

# Crear postes
pos_x = (pergola_largo - poste_lado) / 2
pos_y = (pergola_ancho - poste_lado) / 2
posiciones_postes = [
    (pos_x, pos_y, poste_alto / 2),
    (-pos_x, pos_y, poste_alto / 2),
    (pos_x, -pos_y, poste_alto / 2),
    (-pos_x, -pos_y, poste_alto / 2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    poste = bpy.context.active_object
    poste.name = f'Poste.{i+1:03d}'
    poste.dimensions = (poste_lado, poste_lado, poste_alto)

# Crear vigas principales (a lo largo)
loc_z_viga = poste_alto + viga_alto / 2
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, pos_y, loc_z_viga))
viga1 = bpy.context.active_object
viga1.name = 'VigaPrincipal.001'
viga1.dimensions = (pergola_largo, poste_lado, viga_alto)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -pos_y, loc_z_viga))
viga2 = bpy.context.active_object
viga2.name = 'VigaPrincipal.002'
viga2.dimensions = (pergola_largo, poste_lado, viga_alto)

# Crear travesaños (emparrillado)
num_travesanos = 7
espaciado = pergola_largo / (num_travesanos - 1)

for i in range(num_travesanos):
    x = -pergola_largo / 2 + i * espaciado
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, loc_z_viga + viga_alto/2 + poste_lado/2))
    travesano = bpy.context.active_object
    travesano.name = f'Travesano.{i+1:03d}'
    travesano.dimensions = (poste_lado, pergola_ancho, poste_lado)