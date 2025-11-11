import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros
ancho_x = 4.0
largo_y = 5.0
ancho_viga = 0.10
alto_viga = 0.15
altura_techo = 2.8

def crear_viga(nombre, escala, posicion):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=escala, location=posicion)
    viga = bpy.context.active_object
    viga.name = nombre
    return viga

# Crear placa base del techo
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, altura_techo), scale=(ancho_x, largo_y, 1))
base_techo = bpy.context.active_object
base_techo.name = 'BaseTecho'

# Crear vigas en dirección Y (a lo largo de X)
num_vigas_y = int(ancho_x) + 1
for i in range(num_vigas_y):
    x_pos = -ancho_x / 2 + i
    escala = (ancho_viga, largo_y, alto_viga)
    posicion = (x_pos, 0, altura_techo - alto_viga / 2)
    crear_viga(f'Viga_Y_{i}', escala, posicion)

# Crear vigas en dirección X (a lo largo de Y)
num_vigas_x = int(largo_y) + 1
for i in range(num_vigas_x):
    y_pos = -largo_y / 2 + i
    escala = (ancho_x, ancho_viga, alto_viga)
    posicion = (0, y_pos, altura_techo - alto_viga / 2)
    crear_viga(f'Viga_X_{i}', escala, posicion)