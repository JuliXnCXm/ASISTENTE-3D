import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
largo_ext = 2.0
ancho_ext = 0.5
alto_ext = 0.6
grosor_pared = 0.05

# --- Dimensiones internas ---
largo_int = largo_ext - 2 * grosor_pared
ancho_int = ancho_ext - 2 * grosor_pared
alto_tierra = alto_ext - 0.1
alto_base = grosor_pared

# --- Crear las 5 paredes de la jardinera ---
# Base
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto_base / 2))
base = bpy.context.active_object
base.name = "Jardinera.Base"
base.dimensions = (largo_ext, ancho_ext, alto_base)

# Pared Larga 1
bpy.ops.mesh.primitive_cube_add(location=(0, (ancho_ext - grosor_pared) / 2, (alto_ext + alto_base)/2))
pared1 = bpy.context.active_object
pared1.name = "Jardinera.ParedLarga1"
pared1.dimensions = (largo_ext, grosor_pared, alto_ext - alto_base)

# Pared Larga 2
bpy.ops.mesh.primitive_cube_add(location=(0, -(ancho_ext - grosor_pared) / 2, (alto_ext + alto_base)/2))
pared2 = bpy.context.active_object
pared2.name = "Jardinera.ParedLarga2"
pared2.dimensions = (largo_ext, grosor_pared, alto_ext - alto_base)

# Pared Corta 1
bpy.ops.mesh.primitive_cube_add(location=((largo_ext - grosor_pared) / 2, 0, (alto_ext + alto_base)/2))
pared3 = bpy.context.active_object
pared3.name = "Jardinera.ParedCorta1"
pared3.dimensions = (grosor_pared, ancho_int, alto_ext - alto_base)

# Pared Corta 2
bpy.ops.mesh.primitive_cube_add(location=(-(largo_ext - grosor_pared) / 2, 0, (alto_ext + alto_base)/2))
pared4 = bpy.context.active_object
pared4.name = "Jardinera.ParedCorta2"
pared4.dimensions = (grosor_pared, ancho_int, alto_ext - alto_base)

# --- Crear la tierra ---
profundidad_tierra = alto_tierra - grosor_pared
bpy.ops.mesh.primitive_cube_add(location=(0, 0, grosor_pared + profundidad_tierra / 2))
tierra = bpy.context.active_object
tierra.name = "TierraJardinera"
tierra.dimensions = (largo_int, ancho_int, profundidad_tierra)