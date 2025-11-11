import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

dim_x = 5.0
dim_y = 4.0
altura = 2.6
espesor_muro = 0.15
espesor_losa = 0.2

def crear_muro(nombre, escala, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=escala, location=ubicacion)
    bpy.context.active_object.name = nombre

# Losa de piso
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(dim_x / 2, dim_y / 2, -espesor_losa / 2),
    scale=(dim_x + 2 * espesor_muro, dim_y + 2 * espesor_muro, espesor_losa)
)
bpy.context.active_object.name = 'LosaSuelo'

# Muros
loc_z = altura / 2
# Muro Norte (Fondo)
crear_muro('MuroNorte', (dim_x, espesor_muro, altura), (dim_x / 2, dim_y + espesor_muro / 2, loc_z))
# Muro Sur (Frente)
crear_muro('MuroSur', (dim_x, espesor_muro, altura), (dim_x / 2, -espesor_muro / 2, loc_z))
# Muro Este (Derecha)
crear_muro('MuroEste', (espesor_muro, dim_y + 2 * espesor_muro, altura), (dim_x + espesor_muro / 2, dim_y / 2, loc_z))
# Muro Oeste (Izquierda)
crear_muro('MuroOeste', (espesor_muro, dim_y + 2 * espesor_muro, altura), (-espesor_muro / 2, dim_y / 2, loc_z))