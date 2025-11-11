import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
lado_largo = 1.5
lado_corto = 1.2
profundidad = 0.6
altura = 0.75
grosor_tablero = 0.05

# Crear las dos partes del tablero
# Parte larga
bpy.ops.mesh.primitive_cube_add(
    location=(lado_largo/2, -profundidad/2, altura - grosor_tablero/2),
    scale=(lado_largo, profundidad, grosor_tablero)
)
parte_larga = bpy.context.active_object
parte_larga.name = 'Tablero_Largo'

# Parte corta
bpy.ops.mesh.primitive_cube_add(
    location=(-profundidad/2, lado_corto/2, altura - grosor_tablero/2),
    scale=(profundidad, lado_corto, grosor_tablero)
)
parte_corta = bpy.context.active_object
parte_corta.name = 'Tablero_Corto'

# Unir las dos partes con un modificador booleano
bool_mod = parte_larga.modifiers.new(name='Union', type='BOOLEAN')
bool_mod.operation = 'UNION'
bool_mod.object = parte_corta
bpy.context.view_layer.objects.active = parte_larga
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

# Eliminar el segundo objeto ya unido
bpy.data.objects.remove(parte_corta)
parte_larga.name = 'Escritorio_L'