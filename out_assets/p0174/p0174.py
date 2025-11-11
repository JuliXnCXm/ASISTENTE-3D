import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 3.0
ancho = 1.0
alto = 0.6
grosor = 0.1

# Crear el volumen exterior
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto / 2), scale=(largo, ancho, alto))
ext = bpy.context.active_object
ext.name = "JardineraExterior"

# Crear el volumen interior para vaciar
largo_int = largo - 2 * grosor
ancho_int = ancho - 2 * grosor
alto_int = alto

bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto / 2), scale=(largo_int, ancho_int, alto_int))
int_vaciado = bpy.context.active_object
int_vaciado.name = "VaciadoJardinera"

# Aplicar modificador booleano
bool_mod = ext.modifiers.new(name='BooleanVaciado', type='BOOLEAN')
bool_mod.object = int_vaciado
bool_mod.operation = 'DIFFERENCE'

# Aplicar el modificador y eliminar el objeto de corte
bpy.context.view_layer.objects.active = ext
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(int_vaciado, do_unlink=True)

# Crear base/suelo de la jardinera
bpy.ops.mesh.primitive_cube_add(location=(0, 0, grosor / 2), scale=(largo_int, ancho_int, grosor))
base = bpy.context.active_object
base.name = "BaseJardinera"