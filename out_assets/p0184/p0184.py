import bpy

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
tam_pergola = 4.0
altura_poste = 3.0
tam_poste = 0.2
viga_ancho = 0.1
viga_alto = 0.2
num_vigas_transversales = 7

# Crear postes
posiciones_postes = [
    (tam_pergola/2, tam_pergola/2, altura_poste/2),
    (-tam_pergola/2, tam_pergola/2, altura_poste/2),
    (-tam_pergola/2, -tam_pergola/2, altura_poste/2),
    (tam_pergola/2, -tam_pergola/2, altura_poste/2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    poste = bpy.context.active_object
    poste.name = f"Poste_{i+1}"
    poste.dimensions = (tam_poste, tam_poste, altura_poste)

# Crear vigas principales (largueros)
pos_viga_y = tam_pergola/2 - tam_poste/2
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, pos_viga_y, altura_poste + viga_alto/2))
larguero1 = bpy.context.active_object
larguero1.name = "Larguero_1"
larguero1.dimensions = (tam_pergola + tam_poste, viga_ancho, viga_alto)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -pos_viga_y, altura_poste + viga_alto/2))
larguero2 = bpy.context.active_object
larguero2.name = "Larguero_2"
larguero2.dimensions = (tam_pergola + tam_poste, viga_ancho, viga_alto)

# Crear vigas transversales
step = tam_pergola / (num_vigas_transversales - 1)
for i in range(num_vigas_transversales):
    pos_x = -tam_pergola/2 + i * step
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x, 0, altura_poste + viga_alto/2))
    viga = bpy.context.active_object
    viga.name = f"VigaTransversal_{i+1}"
    viga.dimensions = (viga_ancho, tam_pergola, viga_alto)