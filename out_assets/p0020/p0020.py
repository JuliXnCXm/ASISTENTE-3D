import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
profundidad = 0.6
altura = 0.9
lado_largo = 3.0 # en eje X
lado_corto = 2.0 # en eje Y
espesor_encimera = 0.04
espesor_panel = 0.02

# Crear el segmento largo
loc_largo = (lado_largo / 2, profundidad / 2, altura - espesor_encimera / 2)
scale_largo = (lado_largo, profundidad, espesor_encimera)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_largo)
encimera_larga = bpy.context.active_object
encimera_larga.name = "EncimeraLarga"
encimera_larga.scale = scale_largo

# Crear el segmento corto
longitud_corta_real = lado_corto - profundidad
loc_corto = (lado_largo - profundidad / 2, profundidad + longitud_corta_real / 2, altura - espesor_encimera / 2)
scale_corto = (profundidad, longitud_corta_real, espesor_encimera)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_corto)
encimera_corta = bpy.context.active_object
encimera_corta.name = "EncimeraCorta"
encimera_corta.scale = scale_corto

# Crear faldón/base para el segmento largo
altura_base = altura - espesor_encimera
loc_base_larga = (lado_largo / 2, profundidad / 2 - espesor_panel/2, altura_base / 2)
scale_base_larga = (lado_largo, espesor_panel, altura_base)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_base_larga)
base_larga = bpy.context.active_object
base_larga.name = "BaseLarga"
base_larga.scale = scale_base_larga

# Crear faldón/base para el segmento corto
loc_base_corta = (lado_largo - profundidad / 2 + espesor_panel/2, profundidad + longitud_corta_real / 2, altura_base / 2)
scale_base_corta = (espesor_panel, longitud_corta_real, altura_base)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_base_corta)
base_corta = bpy.context.active_object
base_corta.name = "BaseCorta"
base_corta.scale = scale_base_corta