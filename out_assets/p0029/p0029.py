import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 1.5
ancho = 0.4
alto = 0.45
espesor_asiento = 0.05
ancho_pata = 0.1

altura_patas = alto - espesor_asiento

# Asiento
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo/2, 0, alto - espesor_asiento/2),
    scale=(largo, ancho, espesor_asiento)
)
asiento = bpy.context.active_object
asiento.name = 'AsientoBanco'

# Pata 1
pos_x_pata1 = ancho_pata / 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(pos_x_pata1, 0, altura_patas/2),
    scale=(ancho_pata, ancho, altura_patas)
)
pata1 = bpy.context.active_object
pata1.name = 'PataIzquierda'

# Pata 2
pos_x_pata2 = largo - ancho_pata / 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(pos_x_pata2, 0, altura_patas/2),
    scale=(ancho_pata, ancho, altura_patas)
)
pata2 = bpy.context.active_object
pata2.name = 'PataDerecha'