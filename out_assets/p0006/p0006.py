import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 5.0
ancho = 4.0
alto = 2.8
espesor = 0.15

# Muro Norte (largo)
bpy.ops.mesh.primitive_cube_add(size=1, location=(largo/2, ancho - espesor/2, alto/2), scale=(largo, espesor, alto))

# Muro Sur (largo)
bpy.ops.mesh.primitive_cube_add(size=1, location=(largo/2, espesor/2, alto/2), scale=(largo, espesor, alto))

# Muro Este (ancho)
bpy.ops.mesh.primitive_cube_add(size=1, location=(largo - espesor/2, ancho/2, alto/2), scale=(espesor, ancho - 2*espesor, alto))

# Muro Oeste (ancho)
bpy.ops.mesh.primitive_cube_add(size=1, location=(espesor/2, ancho/2, alto/2), scale=(espesor, ancho - 2*espesor, alto))