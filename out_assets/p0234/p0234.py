import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 4.0
ancho = 1.0
alto = 0.8
grosor = 0.1

# Base
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(largo/2, ancho/2, grosor/2), 
    scale=(largo, ancho, grosor)
)
bpy.context.active_object.name = "Jardinera.Base"

# Pared Larga 1 (Frontal)
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(largo/2, grosor/2, alto/2 + grosor/2),
    scale=(largo, grosor, alto)
)
bpy.context.active_object.name = "Jardinera.ParedLarga.Frontal"

# Pared Larga 2 (Trasera)
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(largo/2, ancho - grosor/2, alto/2 + grosor/2),
    scale=(largo, grosor, alto)
)
bpy.context.active_object.name = "Jardinera.ParedLarga.Trasera"

# Pared Corta 1 (Izquierda)
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(grosor/2, ancho/2, alto/2 + grosor/2),
    scale=(grosor, ancho - 2*grosor, alto)
)
bpy.context.active_object.name = "Jardinera.ParedCorta.Izquierda"

# Pared Corta 2 (Derecha)
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(largo - grosor/2, ancho/2, alto/2 + grosor/2),
    scale=(grosor, ancho - 2*grosor, alto)
)
bpy.context.active_object.name = "Jardinera.ParedCorta.Derecha"