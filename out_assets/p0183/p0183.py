import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 3.0
ancho = 0.8
alto = 0.6
grosor = 0.1

# Crear el volumen exterior
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto / 2))
exterior = bpy.context.active_object
exterior.name = "Jardinera_Exterior"
exterior.dimensions = (largo, ancho, alto)

# Crear el volumen interior para el hueco
largo_int = largo - 2 * grosor
ancho_int = ancho - 2 * grosor
alto_int = alto - grosor # Hueco hasta el fondo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, (alto_int / 2) + grosor))
interior = bpy.context.active_object
interior.name = "Jardinera_Hueco"
interior.dimensions = (largo_int, ancho_int, alto_int)

# Aplicar modificador booleano para hacer el hueco
bool_mod = exterior.modifiers.new(name='BooleanHollow', type='BOOLEAN')
bool_mod.object = interior
bool_mod.operation = 'DIFFERENCE'
bpy.context.view_layer.objects.active = exterior
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

# Eliminar el objeto del hueco
bpy.data.objects.remove(interior, do_unlink=True)