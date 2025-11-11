import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 2.0
ancho = 0.5
alto = 0.6
grosor_pared = 0.05

# Crear el volumen exterior
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto / 2), scale=(largo / 2, ancho / 2, alto / 2))
ext = bpy.context.active_object
ext.name = 'JardineraExterior'

# Crear el volumen interior para el hueco
largo_int = largo - 2 * grosor_pared
ancho_int = ancho - 2 * grosor_pared
alto_int = alto - grosor_pared
bpy.ops.mesh.primitive_cube_add(location=(0, 0, grosor_pared + alto_int / 2), scale=(largo_int / 2, ancho_int / 2, alto_int / 2))
int = bpy.context.active_object
int.name = 'JardineraInterior'

# Aplicar booleana
bool_mod = ext.modifiers.new(name='HacerHueco', type='BOOLEAN')
bool_mod.object = int
bool_mod.operation = 'DIFFERENCE'
bpy.context.view_layer.objects.active = ext
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(int)

# Crear la tierra
alto_tierra = alto - 0.10 # 10 cm del borde
loc_z_tierra = grosor_pared + (alto_tierra - grosor_pared) / 2
bpy.ops.mesh.primitive_cube_add(location=(0, 0, loc_z_tierra), scale=(largo_int / 2, ancho_int / 2, (alto_tierra - grosor_pared) / 2))
tierra = bpy.context.active_object
tierra.name = 'TierraJardinera'