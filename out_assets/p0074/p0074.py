import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
alto = 1.8
ancho = 1.0
fondo = 0.3
espesor = 0.02
num_estantes = 5

# Crear panel lateral izquierdo
ancho_int = ancho - 2 * espesor
pos_x_izq = -ancho_int / 2.0 - espesor / 2.0
bpy.ops.mesh.primitive_cube_add(
    location=(pos_x_izq, 0, alto / 2.0),
    scale=(espesor, fondo, alto)
)
bpy.context.object.name = 'PanelIzquierdo'

# Crear panel lateral derecho
pos_x_der = ancho_int / 2.0 + espesor / 2.0
bpy.ops.mesh.primitive_cube_add(
    location=(pos_x_der, 0, alto / 2.0),
    scale=(espesor, fondo, alto)
)
bpy.context.object.name = 'PanelDerecho'

# Crear estantes
espacio_entre_estantes = (alto - espesor) / (num_estantes - 1)
for i in range(num_estantes):
    altura_estante = (i * espacio_entre_estantes) + espesor / 2.0
    # El estante inferior va a Z=0
    if i == 0:
        altura_estante = espesor / 2.0
    # El estante superior va al tope
    if i == num_estantes - 1:
        altura_estante = alto - espesor / 2.0

    bpy.ops.mesh.primitive_cube_add(
        location=(0, 0, altura_estante),
        scale=(ancho_int, fondo, espesor)
    )
    bpy.context.object.name = f'Estante_{i+1}'