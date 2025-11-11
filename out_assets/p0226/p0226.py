import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_ext = 2.0
ancho_ext = 0.6
alto_ext = 0.5
grosor = 0.05

# Base
bpy.ops.mesh.primitive_cube_add(location=(0, 0, grosor / 2))
base = bpy.context.active_object
base.name = "Jardinera.Base"
base.dimensions = (largo_ext, ancho_ext, grosor)

# Pared Larga 1
bpy.ops.mesh.primitive_cube_add(location=(0, (ancho_ext - grosor) / 2, alto_ext / 2 + grosor / 2))
pared_l1 = bpy.context.active_object
pared_l1.name = "Jardinera.ParedLarga.1"
pared_l1.dimensions = (largo_ext, grosor, alto_ext)

# Pared Larga 2
bpy.ops.mesh.primitive_cube_add(location=(0, -(ancho_ext - grosor) / 2, alto_ext / 2 + grosor / 2))
pared_l2 = bpy.context.active_object
pared_l2.name = "Jardinera.ParedLarga.2"
pared_l2.dimensions = (largo_ext, grosor, alto_ext)

# Pared Corta 1
bpy.ops.mesh.primitive_cube_add(location=((largo_ext - grosor) / 2, 0, alto_ext / 2 + grosor / 2))
pared_c1 = bpy.context.active_object
pared_c1.name = "Jardinera.ParedCorta.1"
pared_c1.dimensions = (grosor, ancho_ext - 2 * grosor, alto_ext)

# Pared Corta 2
bpy.ops.mesh.primitive_cube_add(location=(-(largo_ext - grosor) / 2, 0, alto_ext / 2 + grosor / 2))
pared_c2 = bpy.context.active_object
pared_c2.name = "Jardinera.ParedCorta.2"
pared_c2.dimensions = (grosor, ancho_ext - 2 * grosor, alto_ext)